# Python
from typing             import List
import sqlalchemy.orm   as _orm

# Schemas
import schemas.lov_vals as lv_schema
import schemas.schema   as schema

# Services
import services.model as m_service

# Ustils
from utils          import constants
from utils.messages import not_found_message, exist_message

# FastApi
from fastapi import status, APIRouter, Depends, Path, HTTPException

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
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Obtener todas las Lov LovVals

    ### Con este servicio obtendremos todas las LovVals
    """
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
    db: _orm.Session = Depends(m_service.get_db)
):
    """
    ## Buscar una LovVals por su ID 

    ### Con este servicio obtendremos solo una LovVals por su ID

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    """
    lov_vals = await m_service.search_by_id(constants.LOV_VALS, id, db)

    if lov_vals is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lov Vals"))

    return lov_vals


@lov_vals.post(
    path            = endpoint + constants.SAVE,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_201_CREATED,
    summary         = "Guarda una LovVals",
    tags            = [tags]
)
async def save(
    input   : lv_schema.SaveLovVals, 
    db      : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Insertar una LovVals

    ### Con este servicio podremos guardar una LovVals con un Id de LOV:

    ### Validaciones a tener en consideración:
    - Valida que id de idlov si exista.
    - Valida que la descripción no exista.
    """
    lov = await m_service.search_by_id(constants.LOV, input.lov_id, db)

    if lov is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lista de Valor"))

    lov_vals = await m_service.search_by_description(constants.LOV_VALS, input.description, db)

    if lov_vals is not None:
        raise HTTPException(status_code = 400, detail = exist_message("Lov Vals"))

    return await m_service.save(constants.LOV_VALS, True, input, db)

@lov_vals.put(
    path            = endpoint + constants.UPDATE,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza LovVals por su descripción",
    tags            = [tags]
)
async def update(
    input   : lv_schema.SaveLovVals, 
    db      : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Actualiza una LovVals

    ### Con este servicio podremos actualizar por descripción de LovVals (no actualiza la descripción). 

    ### Validaciones a tener en consideración:
    - Valida que ID de Lista de Valor si exista.
    - Valida que la descripción de LovVals exista.
    """
    lov = await m_service.search_by_id(constants.LOV, input.idlov, db)

    if lov is None:
        raise HTTPException(status_code = 404, detail = not_found_message("Lista de Valor"))

    lov_vals = await m_service.search_by_description(constants.LOV_VALS, input.description, db)

    if lov_vals is None:
        raise HTTPException(status_code = 404, detail = exist_message("LovVals"))

    lov_vals.idlov      = input.idlov
    lov_vals.active     = input.active
    lov_vals.comment    = input.comment
    lov_vals.skill      = input.skill

    return await m_service.save(constants.LOV_VALS, False, lov_vals, db)

@lov_vals.patch(
    path            = endpoint + constants.UPDATE_DESCRIPTION,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza la descripcion lista de valores",
    tags            = [tags]
)
async def update_description(
    lovvalsInput    : schema.UpdateDescriptionModel, 
    db              : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Actualiza la descripción de un LovVals

    ### Con este servicio podremos actualizar la descripción de la lista de valores, por el id (Solo actualiza la descripción)

    ### Validaciones a tener en consideración:
    - Valida que la descripción no exista
    - Valida que id de idlovvals si exista
    """
    lov_vals = await m_service.search_by_id(constants.LOV_VALS, lovvalsInput.idlovvals, db)

    if lov_vals is None:
        raise HTTPException(status_code = 404, detail = "Lov Vals no existe, favor ingresa otra.")

    if await m_service.search_by_description(constants.LOV_VALS, lovvalsInput.description, db) is not None:
        raise HTTPException(status_code = 400, detail = "La descripción de este Lov Vals ya existe.")

    lov_vals.description = lovvalsInput.description

    return await m_service.save(constants.LOV_VALS, False, lov_vals, db)


@lov_vals.patch(
    path            = endpoint + constants.UPDATE_SKILL,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza el valor JSON skill de LovVals",
    tags            = [tags]
)
async def update_skill(
    lovvalsInput    : lv_schema.UpdateSkillLovVals, 
    db              : _orm.Session = Depends(m_service.get_db),
):
    """
    ## Actualizar la Skill de LovVals

    ### Con este servicio podremos actualizar la Skill de la lista de valores, por la descripción.

    ### Validaciones a tener en consideración:
    - Valida que la descripción exista.
    """
    lov_vals = await m_service.search_by_description(constants.LOV_VALS, lovvalsInput.description, db)

    if lov_vals is None:
        raise HTTPException(status_code = 404, detail = "Lov Vals no existe, favor ingresa otra.")

    lov_vals.skill = lovvalsInput.skill

    return await m_service.save(constants.LOV_VALS, False, lov_vals, db)
