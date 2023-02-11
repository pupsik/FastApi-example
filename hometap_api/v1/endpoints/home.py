from dataclasses import dataclass, field

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

from hometap_api.secrets import SecretStore
from hometap_api.v1.clients.house_canary import HouseCanaryAPIClient
from hometap_api.v1.models.hc_response import GeoCodeResponse, PropertyDetailsResponse
from hometap_api.v1.models.response import HasSepticSystemResponse, HelloWorldResponse
from hometap_api.v1.settings import SETTINGS


@dataclass
class Endpoint:
    prefix: str
    router: APIRouter = field(default_factory=APIRouter)


endpoint = Endpoint(prefix="/api")


@endpoint.router.get("/")
async def read_home() -> HelloWorldResponse:
    return {"hello": "world"}


@endpoint.router.get("/has_septic_system")
async def has_septic_system(address: str) -> HasSepticSystemResponse:
    client = HouseCanaryAPIClient(
        auth=(
            SETTINGS.house_canary_key,
            SecretStore.get_secret(
                SETTINGS.house_canary_key, directory=SETTINGS.secrets_dir
            ),
        )
    )

    # First, we need to try and convert user-supplied address
    # into House Carany "cananonical address"

    geocode_resp = client.get("property/geocode", params=address).json()
    # Validate the response structure matches our expectations
    try:
        GeoCodeResponse(**geocode_resp)
    except ValidationError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content="Unable to validate responses from House Canary API. \
            Service will be unavailable until validation errors are resolved.",
        )

    if geocode_resp["status"]["match"]:
        canonical_address = geocode_resp["address_info"]["slug"]
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Unable to validate user supplied property address",
        )
    # Using verified address, get sewer status
    details_resp = client.get("property/details", params=canonical_address).json()

    # Validate the response structure matches our expectations
    try:
        PropertyDetailsResponse(**details_resp)
    except ValidationError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content="Unable to validate responses from House Canary API. \
            Service will be unavailable until validation errors are resolved.",
        )

    sewer = details_resp["property/details"]["result"]["property"]["sewer"]
    if sewer.lower() == "septic":
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"has_septic_system": True}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"has_septic_system": False}
        )
