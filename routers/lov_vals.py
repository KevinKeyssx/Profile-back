# Python
from typing             import List
import sqlalchemy.orm   as _orm

# Schemas
import schemas.lov_vals as lv_schema

# Services
import services.model as m_service

# Ustils
from utils          import constants
from utils.messages import not_found_message

# FastApi
from fastapi import status, APIRouter, Depends, Path, HTTPException, Header

from utils.utils import validateToken

lov_vals    = APIRouter()
version     = "/api/v1/"
endpoint    = version + "lov-vals/"
tags        = "Lov Vals"

@lov_vals.get(
    path            = endpoint + constants.SEARCH_ALL,
    response_model  = List[lv_schema.GetLovVals],
    status_code     = status.HTTP_200_OK,
    summary         = "Busca todo el detalle de LovVals hija de LOV",
    tags            = [tags]
)
async def search_all(
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends(m_service.get_db)
):
    """
    ## Obtener todas las Lov LovVals

    ### Con este servicio obtendremos todas las LovVals
    """
    validateToken( headers )
    return await m_service.search_all(constants.LOV_VALS, db)


@lov_vals.get(
    path            = endpoint + constants.SEARCH_BY_ID,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Busca una LovVals por su ID",
    tags            = [tags]
)
async def search_by_id(
    id: int     = Path(
        ..., 
        gt          = 0,
        title       = "Identificador",
        description = "Id de Lov Vals",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar una LovVals por su ID 

    ### Con este servicio obtendremos solo una LovVals por su ID

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    """
    validateToken( headers )
    lov_vals = await m_service.search_by_id(constants.LOV_VALS, id, db)

    if lov_vals is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lov Vals"))

    return lov_vals
