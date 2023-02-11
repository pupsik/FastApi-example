"""
Response models for House Canary Responses 
"""

from typing import List

from pydantic import BaseModel, Field


class GeoCodeApiStats(BaseModel):
    api_code: int
    api_code_description: str
    result: bool


class GeoCodeAddressInfo(BaseModel):
    address_full: str
    slug: str


class GeoCodeStatus(BaseModel):
    match: bool
    errors: List[str]


class GeoCodeResponse(BaseModel):
    property_geocode: GeoCodeApiStats = Field(..., alias="property/geocode")
    address_info: GeoCodeAddressInfo
    status: GeoCodeStatus


class PropertyDetailsProperty(BaseModel):
    air_conditioning: str
    sewer: str
    style: str
    pool: bool


class PropertyDetailsResult(BaseModel):
    property: PropertyDetailsProperty


class PropertyDetails(BaseModel):
    api_code_description: str
    api_code: int
    result: PropertyDetailsResult


class PropertyDetailsResponse(BaseModel):
    property_details: PropertyDetails = Field(..., alias="property/details")
