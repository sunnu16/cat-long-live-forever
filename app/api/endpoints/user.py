@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    response = users.get_user_id(user_id=user_id, db=db)

    return response
