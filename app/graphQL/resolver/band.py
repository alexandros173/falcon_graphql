from typing import List

from ariadne import ObjectType, QueryType, convert_kwargs_to_snake_case
from graphql import GraphQLResolveInfo
from dependency_injector.wiring import Provide, inject

from app.container import AppContainer
from app.models.graphQL.band_information import BandInformation

query = QueryType()
band_schema = ObjectType("Band")


@query.field("getMusicalBandsInformation")
@convert_kwargs_to_snake_case
@inject
def get_bands_information(item,
                          bands_service=Provide[AppContainer.services.band_service]) -> BandInformation:
    try:
        return bands_service.get_bands_information(item)
    except Exception as e:
        print(f'Exception when querying band service')
