# Python
from typing             import List
import sqlalchemy.orm   as _orm

# Schemas
import schemas.schema   as schema
import schemas.lov_vals as lv_schema

# Services
import services.model as m_service

# Utils
from utils          import constants
from utils.messages import not_found_message, exist_message

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


@lov_vals.post(
    path            = endpoint + constants.SAVE,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_201_CREATED,
    summary         = "Guarda una LovVals",
    tags            = [ tags ]
)
async def save(
    input   : lv_schema.SaveLovVals,
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> lv_schema.GetLovVals:
    """
    ## Insertar una LovVals

    ### Con este servicio podremos guardar una LovVals vinculada a un ID de LOV

    ### Validaciones a tener en consideración:
    - Valida que el ID de Lista de Valor exista.
    - Valida que la descripción no exista previamente.
    """
    validateToken( headers )

    lov = await m_service.search_by_id( constants.LOV, input.lov_id, db )

    if ( lov is None ):
        raise HTTPException( status_code = 404, detail = not_found_message( "Lista de Valor" ) )

    lov_vals = await m_service.search_by_description( constants.LOV_VALS, input.description, db )

    if ( lov_vals is not None ):
        raise HTTPException( status_code = 400, detail = exist_message( "Lov Vals" ) )

    return await m_service.save( constants.LOV_VALS, True, input, db )


@lov_vals.patch(
    path            = endpoint + constants.UPDATE,
    response_model  = lv_schema.GetLovVals,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza parcialmente una LovVals por su ID",
    tags            = [ tags ]
)
async def update(
    input   : schema.UpdatePatchModel,
    id      : int = Path(
        ...,
        gt          = 0,
        title       = "Identificador",
        description = "Id de Lov Vals a actualizar",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> lv_schema.GetLovVals:
    """
    ## Actualiza parcialmente una LovVals

    ### Con este servicio podremos modificar description, active, skill y/o comment de LovVals por su ID

    ### Validaciones a tener en consideración:
    - Valida que el ID de LovVals exista.
    - Valida que la nueva descripción no exista en otro registro.
    """
    validateToken( headers )

    lov_vals = await m_service.search_by_id( constants.LOV_VALS, id, db )

    if ( lov_vals is None ):
        raise HTTPException( status_code = 404, detail = not_found_message( "Lov Vals" ) )

    if ( input.description is not None ):
        lov_by_desc = await m_service.search_by_description( constants.LOV_VALS, input.description, db )
        if ( lov_by_desc is not None and lov_by_desc.id != id ):
            raise HTTPException( status_code = 400, detail = exist_message( "Lov Vals" ) )
        lov_vals.description = input.description

    if ( input.active is not None ):
        lov_vals.active = input.active

    if ( input.skill is not None ):
        lov_vals.skill = input.skill

    if ( input.comment is not None ):
        lov_vals.comment = input.comment

    return await m_service.save( constants.LOV_VALS, False, lov_vals, db )


@lov_vals.delete(
    path            = endpoint + constants.DELETE_BY_ID,
    response_model  = bool,
    status_code     = status.HTTP_200_OK,
    summary         = "Elimina una LovVals por su ID",
    tags            = [ tags ]
)
async def delete_by_id(
    id      : int = Path(
        ...,
        gt          = 0,
        title       = "Identificador",
        description = "Id de Lov Vals a eliminar",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> bool:
    """
    ## Eliminar una LovVals por su ID

    ### Con este servicio podremos eliminar un registro específico de LovVals

    ### Validaciones a tener en consideración:
    - Valida que el ID ingresado exista.
    """
    validateToken( headers )

    lov_vals = await m_service.search_by_id( constants.LOV_VALS, id, db )

    if ( lov_vals is None ):
        raise HTTPException( status_code = 404, detail = not_found_message( "Lov Vals" ) )

    return await m_service.delete( lov_vals, db )
