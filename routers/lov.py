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
from utils.messages import not_found_message, exist_message
from utils.utils    import validateToken

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
    path            = endpoint + constants.SEARCH_PARENTS,
    response_model  = List[ schema.GetModel ],
    status_code     = status.HTTP_200_OK,
    summary         = "Busca solo los registros padre de la lista de valores",
    tags            = [ tags ]
)
async def search_parents(
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> List[ schema.GetModel ]:
    """
    ## Buscar los registros padre de la lista de valores
    ### Con este servicio obtendremos únicamente los registros padre de la tabla list_of_values sin incluir sus hijos (lov_vals)
    """
    validateToken( headers )
    return await m_service.search_all( constants.LOV, db )


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


@lov.post(
    path            = endpoint + constants.SAVE,
    response_model  = schema.GetModel,
    status_code     = status.HTTP_201_CREATED,
    summary         = "Guarda una lista de valor",
    tags            = [ tags ]
)
async def save(
    input   : schema.SaveModel,
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> schema.GetModel:
    """
    ## Insertar una Lista de Valor

    ### Con este servicio podremos insertar en la tabla de Lista de Valor

    ### Validaciones a tener en consideración:
    - Valida que la descripción no exista previamente.
    """
    validateToken( headers )

    lov = await m_service.search_by_description(
        key         = constants.LOV,
        description = input.description, 
        db          = db
    )

    if ( lov is not None ):
        raise HTTPException( status_code = 400, detail = exist_message( "La descripción de la Lista de valor" ) )

    return await m_service.save(
        key     = constants.LOV,
        insert  = True,
        schema  = input,
        db      = db
    )


@lov.patch(
    path            = endpoint + constants.UPDATE,
    response_model  = schema.GetModel,
    status_code     = status.HTTP_200_OK,
    summary         = "Actualiza parcialmente una lista de valor por su ID",
    tags            = [ tags ]
)
async def update(
    input   : schema.UpdatePatchModel,
    id      : int = Path(
        ...,
        gt          = 0,
        title       = "Identificador",
        description = "Id de la lista de valor a actualizar",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> schema.GetModel:
    """
    ## Actualiza parcialmente una Lista de Valor

    ### Con este servicio podremos modificar description, active, skill y/o comment de la Lista de Valor por su ID

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    - Valida que si se modifica la descripción, esta no exista en otro registro.
    """
    validateToken( headers )

    lov = await m_service.search_by_id( constants.LOV, id, db )

    if ( lov is None ):
        raise HTTPException( status_code = 404, detail = not_found_message( "Lista de Valor" ) )

    if ( input.description is not None ):
        lov_by_desc = await m_service.search_by_description(
            key         = constants.LOV,
            description = input.description,
            db          = db
        )
        if ( lov_by_desc is not None and lov_by_desc.id != id ):
            raise HTTPException( status_code = 400, detail = exist_message( "La descripción de la Lista de valor" ) )
        lov.description = input.description

    if ( input.active is not None ):
        lov.active = input.active

    if ( input.skill is not None ):
        lov.skill = input.skill

    if ( input.comment is not None ):
        lov.comment = input.comment

    return await m_service.save(
        key     = constants.LOV,
        insert  = False,
        schema  = lov,
        db      = db
    )


@lov.delete(
    path            = endpoint + constants.DELETE_BY_ID,
    response_model  = bool,
    status_code     = status.HTTP_200_OK,
    summary         = "Elimina una lista de valor y sus hijos asociados por su ID",
    tags            = [ tags ]
)
async def delete_by_id(
    id      : int = Path(
        ...,
        gt          = 0,
        title       = "Identificador",
        description = "Id de la lista de valor a eliminar",
        example     = 1
    ),
    headers : str = Header(
        alias   = "X-T",
        example = "http",
    ),
    db      : _orm.Session = Depends( m_service.get_db )
) -> bool:
    """
    ## Eliminar una lista de valor en cascada

    ### Con este servicio podremos eliminar una lista de valor por su ID junto a todos sus lov_vals hijos relacionados

    ### Validaciones a tener en consideración:
    - Valida que el id ingresado exista.
    """
    validateToken( headers )

    lov = await m_service.search_by_id( constants.LOV, id, db )

    if ( lov is None ):
        raise HTTPException( status_code = 404, detail = not_found_message( "Lista de valor" ) )

    return await m_service.delete_lov_cascade( id, db )
