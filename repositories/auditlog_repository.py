from models.auditlog_model import AuditLog


def create_audit_log(
    db,
    user_id,
    action,
    entity,
    entity_id,
    old_data=None,
    new_data=None
):

    audit_log = AuditLog(

        user_id=user_id,

        action=action,

        entity=entity,

        entity_id=entity_id,

        old_data=old_data,

        new_data=new_data
    )

    db.add(audit_log)

    db.flush()

    return audit_log