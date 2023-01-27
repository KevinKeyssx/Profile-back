# Python
from typing             import List
import sqlalchemy.orm   as _orm

# Schemas
import schemas.schema   as schema
import schemas.lov_vals as lv_schema

# Services
import services.model as m_service

# FastApi
from fastapi import status, APIRouter, Depends, HTTPException, Path, Header

# Utils
from utils          import constants
from utils.messages import not_found_message
from utils.utils import validateToken

# Variables
lov         = APIRouter()
version     = "/api/v1/"
endpoint    = version + "lov/"
tags        = "List Of Values"

# Services
@lov.get(
    path            = endpoint + constants.SEARCH_ALL,
    response_model  = List[lv_schema.GetInfoLovVals],
    status_code     = status.HTTP_200_OK,
    summary         = "Busca la lista de valores",
    tags            = [tags]
)
async def search_all(
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar todas las lista de valores
    ### Con este servicio obtendremos todas las lista de valores de la tabla Lov
    """
    validateToken( headers )
    lov_list_info   : List[lv_schema.GetInfoLovVals] = []
    all_lovs        : List[schema.GetModel] = await m_service.search_all(constants.LOV, db)

    for lov in all_lovs:
        lov_list_info.append(await lov_vals_in_lov(lov, db))

    return lov_list_info


@lov.get(
    path            = endpoint + constants.SEARCH_BY_ID,
    response_model  = lv_schema.GetInfoLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Busca la lista de valor por su ID",
    tags            = [tags]
)
async def search_by_id(
    id: int     = Path(
        ..., 
        gt          = 0,
        title       = "Lov Vals",
        description = "Id de lov vals",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar la lista de valor

    ### Con este servicio obtendremos una lista de valor por su id de la tabla LOV

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    """
    validateToken( headers )

    lov = await m_service.search_by_id(constants.LOV, id, db)

    if lov is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lista de valor"))

    return await lov_vals_in_lov(lov, db)


async def lov_vals_in_lov(lov: schema.GetModel, db: _orm.Session):
    lov_vals: List[lv_schema.GetLovVals] = await m_service.search_by_lovid(constants.LOV_VALS, lov.id, db)

    return lv_schema.GetInfoLovVals(
        id          = lov.id,
        description = lov.description,
        active      = lov.active,
        created_at  = lov.created_at,
        comment     = lov.comment,
        lov_vals    = [lov_val for lov_val in lov_vals]
    )
