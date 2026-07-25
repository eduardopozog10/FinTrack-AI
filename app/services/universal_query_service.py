from sqlmodel import Session


class UniversalQueryService:

    @staticmethod
    def process(
        session: Session,
        query_filter,
    ):
        """
        Motor unificado de consultas.

        Por ahora solamente imprimiremos el QueryFilter recibido.
        En los siguientes pasos iremos implementando
        cada tipo de consulta.
        """

        print("\n==============================")
        print("UNIVERSAL QUERY SERVICE")
        print(query_filter)
        print("==============================\n")

        return {
            "message": "UniversalQueryService funcionando.",
            "query_filter": str(query_filter),
        }