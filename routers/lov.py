# Python
from typing             import List
import sqlalchemy.orm   as _orm

# Schemas
import schemas.schema   as schema
import schemas.lov_vals as lv_schema

# Services
import services.model as m_service

# FastApi
from fastapi import status, APIRouter, Depends, HTTPException, Path

# Utils
from utils          import constants
from utils.messages import not_found_message, exist_message

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
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar todas las lista de valores
    ### Con este servicio obtendremos todas las lista de valores de la tabla Lov
    """
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
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar la lista de valor

    ### Con este servicio obtendremos una lista de valor por su id de la tabla LOV

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    """
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


@lov.post(
    path            = endpoint + constants.SAVE,
    response_model  = schema.GetModel,
    status_code     = status.HTTP_201_CREATED,
    summary         = "Guarda una lista de valor",
    tags            = [tags]
)
async def save(
    input   : schema.SaveModel,
    db      : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Insertar una Lista de Valor

    ### Con este servicio podremos insetar en la tabla de Lista de Valor:

    ### Validaciones a tener en consideración:
    - Valida que la descripción no exista.
    """
    lov = await m_service.search_by_description(
        key         = constants.LOV,
        description = input.description, 
        db          = db
    )

    if lov is not None:
        raise HTTPException(status_code = 400, detail = exist_message("La descripción de la Lista de valor"))

    return await m_service.save(
        key     = constants.LOV,
        insert  = True,
        schema  = input,
        db      = db
    )

@lov.put(
    path            = endpoint + constants.UPDATE,
    response_model  = schema.GetModel,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza una lista de valor",
    tags            = [tags]
)
async def update(
    input   : schema.SaveModel,
    db      : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Actualiza una Lista de Valor

    ### Con este servicio podremos modificar active y comment por la descripción de la Lista de Valor:

    ### Validaciones a tener en consideración:
    - Valida que la descripción si exista.
    """
    lov = await m_service.search_by_description(
        key         = constants.LOV,
        description = input.description, 
        db          = db
    )

    if lov is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lista de Valor"))

    lov.comment = input.comment
    lov.active  = input.active

    return await m_service.save(
        key     = constants.LOV,
        insert  = False,
        schema  = lov,
        db      = db
    )

@lov.patch(
    path            = endpoint + constants.UPDATE_DESCRIPTION,
    response_model  = schema.GetModel,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza la descripcion lista de valores",
    tags            = [tags]
)
async def update_description(
    input   : schema.UpdateDescriptionModel,
    db      : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Actualiza una Lista de Valor

    ### Con este servicio podremos modificar la descripción por el id:

    ### Validaciones a tener en consideración:
    - Valida que el id si exista.
    - Valida que la descripción no exista.
    """
    lov: schema.GetModel = await m_service.search_by_id(
        key = constants.LOV,
        id  = input.id, 
        db  = db
    )

    if lov is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lista de Valor"))

    lov_description = await m_service.search_by_description(
        key         = constants.LOV,
        description = input.description, 
        db          = db
    )

    if lov_description is not None:
        raise HTTPException(status_code = 400, detail = exist_message("Lista de Valor"))

    lov.description = input.description

    return await m_service.save(
        key     = constants.LOV,
        insert  = False,
        schema  = lov,
        db      = db
    )