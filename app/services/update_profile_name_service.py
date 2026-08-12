from sqlmodel import Session

from app.schemas.ai_command import AICommand
from app.schemas.operation_result import OperationResult
from app.services.user_profile_service import UserProfileService


class UpdateProfileNameService:

    @staticmethod
    def process(
        session: Session,
        command: AICommand,
        user_id: int | None = None,
    ):

        new_name = command.description

        # ==========================================
        # VALIDAR NOMBRE
        # ==========================================

        if not new_name:
            return OperationResult(
                success=False,
                action="profile_name_updated",
                data={
                    "message": (
                        "No pude determinar el nombre "
                        "que quieres utilizar."
                    ),
                },
            )

        new_name = new_name.strip()

        if not new_name:
            return OperationResult(
                success=False,
                action="profile_name_updated",
                data={
                    "message": (
                        "No pude determinar el nombre "
                        "que quieres utilizar."
                    ),
                },
            )

        # ==========================================
        # VALIDAR USUARIO
        # ==========================================

        if user_id is None:
            return OperationResult(
                success=False,
                action="profile_name_updated",
                data={
                    "message": (
                        "No pude identificar tu usuario."
                    ),
                },
            )

        # ==========================================
        # ACTUALIZAR NOMBRE
        # ==========================================

        user = UserProfileService.update_name(
            session=session,
            user_id=user_id,
            full_name=new_name,
        )

        if user is None:
            return OperationResult(
                success=False,
                action="profile_name_updated",
                data={
                    "message": (
                        "No pude actualizar tu nombre."
                    ),
                },
            )

        return OperationResult(
            success=True,
            action="profile_name_updated",
            data={
                "full_name": user.full_name,
            },
        )