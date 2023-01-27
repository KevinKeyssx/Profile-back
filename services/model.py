# Python
from typing import TYPE_CHECKING, List

# Models
import models.lov       as lov_model

# Schemas
import schemas.lov_vals         as lv_schemas
import schemas.schema           as schema

import database as _database


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


if TYPE_CHECKING:
    from sqlalchemy.orm import Session


schemas: dict = {
    'lov'           : schema.GetModel,
    'lovvals'       : lv_schemas.GetLovVals, 
}


models: dict  = {
    'lov'           : lov_model.Lov, 
    'lovvals'       : lov_model.Lov_Vals, 
}

# Obtener todos los datos un modelo
async def search_all(
    key : str,
    db  : "Session"
) -> List[any]:
    return list(
        map(
            schemas.get(key).from_orm,
            db.query(models.get(key)).all()
        )
    )

# Obtener un modelo por su id
async def search_by_id(
    key : str,
    id  : int, 
    db  : "Session"
) -> any:
    return db.query(
        models.get(key)
    ).filter(
        models.get(key).id == id
    ).first()

# Obtener un modelo por su description
async def search_by_description(
    key         : str,
    description : str,
    db          : "Session"
) -> any:
    return db.query(
        models.get(key)
    ).filter(
        models.get(key).description == description
    ).first()

# Obtener un modelo por su id
async def search_by_lovid_inlovvas(
    lov_id  : int, 
    db      : "Session"
) -> List[lv_schemas.GetLovVals]:
    return db.query(
        lov_model.Lov_Vals
    ).filter(
        lov_model.Lov_Vals.lov_id == lov_id
    ).all()

# Obtener un modelo por su id
async def search_by_lovid(
    key : str,
    id  : int, 
    db  : "Session"
) -> List[lv_schemas.GetLovVals]:
    return db.query(
        models.get(key)
    ).filter(
        models.get(key).lov_id == id
    ).all()

# Obtener un modelo por su id
async def search_by_skill(
    model   : str,
    key     : str,
    value   : any,
    db      : "Session"
) -> any:
    return db.query(
        models.get(model)
    ).filter(
        models.get(model).skill[key] == value
    ).all()

# Elimina un modelo
async def delete(
    model   : any, 
    db      : "Session"
) -> bool:
    db.delete(model)
    db.commit()
    return True