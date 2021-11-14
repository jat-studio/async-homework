import fix_cms_model


def dummy(body: dict) -> None:
    pass


def user_created(body: dict) -> None:
    fix_cms_model.add_user(
        public_id=body["public_id"],
        email=body["email"],
        full_name=body["full_name"],
        role=body["role"],
    )


def user_role_changed(body: dict) -> None:
    fix_cms_model.update_user_role(public_id=body["public_id"], role=body["role"])


def user_updated(body: dict) -> None:
    fix_cms_model.update_user(
        public_id=body["public_id"],
        email=body["email"],
        full_name=body["full_name"],
    )
