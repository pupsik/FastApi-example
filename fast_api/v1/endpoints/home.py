from dataclasses import dataclass, field

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError

from fast_api.secrets import SecretStore
from fast_api.v1.clients.house_canary import HouseCanaryAPIClient
from fast_api.v1.models.hc_response import (GeoCodeResponse,
                                               PropertyDetailsResponse)
from fast_api.v1.models.response import (ExceptionMessage,
                                            HasSepticSystemResponse,
                                            HelloWorldResponse)
from fast_api.v1.settings import SETTINGS

tags_metadata = [
    {
        "name": "has_septic_system",
        "description": "Takes in user provided address, validates the address and \
             returns a True/False response indicating if septic system is present.",
    }
]


@dataclass
class Endpoint:
    prefix: str
    router: APIRouter = field(default_factory=APIRouter)


endpoint = Endpoint(prefix="/api")


@endpoint.router.get("/", include_in_schema=False)
async def read_home() -> HelloWorldResponse:
    return {"hello": "world"}


@endpoint.router.get(
    "/has_septic_system",
    tags=["has_septic_system"],
    responses={503: {"model": ExceptionMessage}, 400: {"model": ExceptionMessage}},
)
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

    geocode_resp = client.get("property/geocode", params={"address": address}).json()
    # Validate the response structure matches our expectations-gives us error-handling \
    # in case House Canary changes response structure without notice
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
    details_resp = client.get(
        "property/details", params={"address": canonical_address}
    ).json()

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
