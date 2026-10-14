"""
==========================================================
 SISTEMA DE REGISTRO Y CONTROL DE ASISTENCIA HOME OFFICE

 Empresa: Tottus - Área de Gestión de Procesos
 Curso: IS275 - Fundamentos de Programación 2

 Grupo 7:
   - Cristhian Giancarlo De la Cruz Saravia
   - Juan José Yzusqui Calderón
   - Omar Alejandro Laime Ccaccro
==========================================================
"""

from datetime import datetime


FORMATO_FECHA = "%d/%m/%Y"
FORMATO_HORA = "%H:%M"
LIMITE_HORAS_SEMANALES = 48


# ==========================================================
# PARTE 1
# INTEGRANTE: CRISTHIAN GIANCARLO DE LA CRUZ SARAVIA
# ROL: MODELO Y CREACIÓN DE OBJETOS
# ==========================================================


# ==========================================================
# CLASE: Colaborador
# ==========================================================

class Colaborador:

    def __init__(self, codigo: str, nombres: str, area: str, aprobador: str):
        self.codigo = codigo
        self.nombres = nombres
        self.area = area
        self.aprobador = aprobador

    def __str__(self):
        return (
            f"[{self.codigo}] {self.nombres} - "
            f"Área: {self.area} - "
            f"Aprobador: {self.aprobador}"
        )


# ==========================================================
# CLASE: Asistencia
# ==========================================================

class Asistencia:

    def __init__(
        self,
        codigo_usuario: str,
        fecha: str,
        hora_inicio: str,
        hora_fin: str
    ):
        self.codigo_usuario = codigo_usuario
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def horas_trabajadas(self) -> float:
        """
        Calcula las horas trabajadas en un registro diario.
        """

        try:
            inicio = datetime.strptime(
                self.hora_inicio,
                FORMATO_HORA
            )

            fin = datetime.strptime(
                self.hora_fin,
                FORMATO_HORA
            )

            diferencia = (
                fin - inicio
            ).total_seconds() / 3600

            # En caso el turno cruce la medianoche
            if diferencia < 0:
                diferencia += 24

            return round(diferencia, 2)

        except ValueError:
            return 0.0

    def __str__(self):

        return (
            f"{self.codigo_usuario:<8} "
            f"{self.fecha:<12} "
            f"{self.hora_inicio:<8} "
            f"{self.hora_fin:<8} "
            f"{self.horas_trabajadas():>6.2f} h"
        )


# ==========================================================
# CLASE PRINCIPAL: GestionAsistencia
# ==========================================================

class GestionAsistencia:

    def __init__(self):

        self.listaColaboradores = []
        self.listaAsistencias = []


    # ======================================================
    # VALIDACIONES
    # ======================================================

    def _validar_texto(self, valor: str) -> bool:

        return (
            valor is not None
            and valor.strip() != ""
        )


    def _validar_fecha(self, valor: str) -> bool:

        try:

            datetime.strptime(
                valor,
                FORMATO_FECHA
            )

            return True

        except ValueError:

            return False


    def _validar_hora(self, valor: str) -> bool:

        try:

            datetime.strptime(
                valor,
                FORMATO_HORA
            )

            return True

        except ValueError:

            return False


    # ======================================================
    # BÚSQUEDAS AUXILIARES
    # ======================================================

    def buscarColaboradorPorCodigo(
        self,
        codigo: str
    ):

        for colaborador in self.listaColaboradores:

            if colaborador.codigo == codigo:

                return colaborador

        return None


    def buscarAsistenciasPorCodigo(
        self,
        codigo: str
    ):

        return [
            asistencia
            for asistencia in self.listaAsistencias
            if asistencia.codigo_usuario == codigo
        ]


    # ======================================================
    # HU01: REGISTRAR COLABORADOR
    # ======================================================

    def registrarColaborador(self):

        print(
            "\n------ REGISTRAR COLABORADOR ------"
        )

        codigo = input(
            "Ingrese código de usuario: "
        ).strip()


        if self.buscarColaboradorPorCodigo(codigo):

            print(
                "Error: ya existe un colaborador "
                "con ese código."
            )

            return


        nombres = input(
            "Ingrese nombres y apellidos: "
        ).strip()

        area = input(
            "Ingrese área: "
        ).strip()

        aprobador = input(
            "Ingrese aprobador (jefe directo): "
        ).strip()


        if not (
            self._validar_texto(codigo)
            and self._validar_texto(nombres)
            and self._validar_texto(area)
            and self._validar_texto(aprobador)
        ):

            print(
                "Error: todos los campos "
                "son obligatorios."
            )

            return


        nuevo = Colaborador(
            codigo,
            nombres,
            area,
            aprobador
        )

        self.listaColaboradores.append(nuevo)


        print(
            "------------------------------------"
        )

        print(
            "Colaborador registrado exitosamente."
        )


    # ======================================================
    # HU02: REGISTRAR ASISTENCIA DIARIA
    # ======================================================

    def registrarAsistencia(self):

        print(
            "\n------ REGISTRAR ASISTENCIA ------"
        )

        codigo = input(
            "Ingrese código de usuario: "
        ).strip()


        colaborador = (
            self.buscarColaboradorPorCodigo(codigo)
        )


        if not colaborador:

            print(
                "Error: el colaborador no existe. "
                "Regístrelo primero (opción 1)."
            )

            return


        fecha = input(
            "Ingrese fecha (dd/mm/aaaa): "
        ).strip()


        if not self._validar_fecha(fecha):

            print(
                "Error: formato de fecha inválido. "
                "Use dd/mm/aaaa."
            )

            return


        hora_inicio = input(
            "Ingrese hora de inicio (hh:mm): "
        ).strip()


        if not self._validar_hora(hora_inicio):

            print(
                "Error: formato de hora inválido. "
                "Use hh:mm (24h)."
            )

            return


        hora_fin = input(
            "Ingrese hora de fin (hh:mm): "
        ).strip()


        if not self._validar_hora(hora_fin):

            print(
                "Error: formato de hora inválido. "
                "Use hh:mm (24h)."
            )

            return


        nueva = Asistencia(
            codigo,
            fecha,
            hora_inicio,
            hora_fin
        )

        self.listaAsistencias.append(nueva)


        print(
            "------------------------------------"
        )

        print(
            "Asistencia registrada correctamente."
        )


    # ======================================================
    # PARTE 2
    # INTEGRANTE: JUAN JOSÉ YZUSQUI CALDERÓN
    # ROL: INTERFAZ, CONSULTAS Y OBSERVER
    # ======================================================


    # ======================================================
    # HU03: LISTAR TODOS LOS REGISTROS
    # ======================================================

    def listarAsistencias(self):

        print(
            "\n=========== LISTADO DE ASISTENCIAS ==========="
        )


        if not self.listaAsistencias:

            print(
                "No hay registros de asistencia."
            )

            return


        print(
            f"{'Código':<8} "
            f"{'Fecha':<12} "
            f"{'Inicio':<8} "
            f"{'Fin':<8} "
            f"{'Horas':>6}"
        )


        for asistencia in self.listaAsistencias:

            print(asistencia)


        print(
            "================================================"
        )

        print(
            f"Total de registros: "
            f"{len(self.listaAsistencias)}"
        )


    # ======================================================
    # HU04: BUSCAR POR CÓDIGO DE USUARIO
    # ======================================================

    def buscarAsistencia(self):

        print(
            "\n------ BUSCAR ASISTENCIA ------"
        )


        codigo = input(
            "Ingrese código de usuario a buscar: "
        ).strip()


        colaborador = (
            self.buscarColaboradorPorCodigo(codigo)
        )

        registros = (
            self.buscarAsistenciasPorCodigo(codigo)
        )


        if not colaborador and not registros:

            print(
                "Colaborador no encontrado."
            )

            return


        print(
            "------------------------------------"
        )


        if colaborador:

            print(
                f"Encontrado: {colaborador}"
            )


        if registros:

            print(
                f"\nRegistros de asistencia "
                f"({len(registros)}):"
            )


            for registro in registros:

                print(registro)

        else:

            print(
                "El colaborador no tiene "
                "registros de asistencia aún."
            )


    # ======================================================
    # HU09: EDITAR REGISTRO DE ASISTENCIA
    # ======================================================

    def editarAsistencia(self):

        print(
            "\n------ EDITAR ASISTENCIA ------"
        )


        codigo = input(
            "Ingrese código de usuario a editar: "
        ).strip()


        fecha = input(
            "Ingrese fecha del registro "
            "a editar (dd/mm/aaaa): "
        ).strip()


        registro = next(
            (
                asistencia
                for asistencia
                in self.listaAsistencias

                if asistencia.codigo_usuario == codigo
                and asistencia.fecha == fecha
            ),
            None
        )


        if not registro:

            print(
                "Registro no encontrado."
            )

            return


        print(
            f"Datos actuales: "
            f"{registro.fecha} | "
            f"{registro.hora_inicio} - "
            f"{registro.hora_fin}"
        )


        nueva_hora_inicio = input(
            "Ingrese nueva hora de inicio "
            "(dejar vacío para no cambiar): "
        ).strip()


        if nueva_hora_inicio:

            if self._validar_hora(
                nueva_hora_inicio
            ):

                registro.hora_inicio = (
                    nueva_hora_inicio
                )

            else:

                print(
                    "Hora de inicio inválida, "
                    "no se modificó."
                )


        nueva_hora_fin = input(
            "Ingrese nueva hora de fin "
            "(dejar vacío para no cambiar): "
        ).strip()


        if nueva_hora_fin:

            if self._validar_hora(
                nueva_hora_fin
            ):

                registro.hora_fin = (
                    nueva_hora_fin
                )

            else:

                print(
                    "Hora de fin inválida, "
                    "no se modificó."
                )


        print(
            "------------------------------------"
        )

        print(
            "Registro actualizado correctamente."
        )


    # ======================================================
    # HU10: ELIMINAR REGISTRO DE ASISTENCIA
    # ======================================================

    def eliminarAsistencia(self):

        print(
            "\n------ ELIMINAR ASISTENCIA ------"
        )


        codigo = input(
            "Ingrese código de usuario a eliminar: "
        ).strip()


        fecha = input(
            "Ingrese fecha del registro: "
        ).strip()


        registro = next(
            (
                asistencia
                for asistencia
                in self.listaAsistencias

                if asistencia.codigo_usuario == codigo
                and asistencia.fecha == fecha
            ),
            None
        )


        if registro:

            self.listaAsistencias.remove(
                registro
            )


            print(
                "------------------------------------"
            )

            print(
                "Registro eliminado exitosamente."
            )

        else:

            print(
                "Registro no encontrado."
            )

    # ======================================================
    # PARTE 3
    # INTEGRANTE: OMAR ALEJANDRO LAIME CCACCRO
    # ROL: CÁLCULOS, DIAGRAMAS E INTEGRACIÓN
    # ======================================================


    # ======================================================
    # HU05, HU06, HU07, HU08
    # RESUMEN DE CÁLCULOS
    # ======================================================

    def resumenCalculos(self):

        print(
            "\n=========== RESUMEN SEMANAL ==========="
        )


        if not self.listaColaboradores:

            print(
                "No hay colaboradores registrados."
            )

            return


        print(
            f"{'Código':<8} "
            f"{'Nombre':<22} "
            f"{'Días':>5} "
            f"{'Hrs.Trab':>9} "
            f"{'Hrs.Extra':>10}"
        )


        codigos_con_asistencia = set()


        for colaborador in self.listaColaboradores:

            registros = (
                self.buscarAsistenciasPorCodigo(
                    colaborador.codigo
                )
            )


            # ----------------------------------------------
            # CÁLCULO DE DÍAS TRABAJADOS
            # ----------------------------------------------

            dias_trabajados = len(
                set(
                    registro.fecha
                    for registro in registros
                )
            )


            # ----------------------------------------------
            # CÁLCULO DE HORAS TRABAJADAS
            # ----------------------------------------------

            horas_totales = round(
                sum(
                    registro.horas_trabajadas()
                    for registro in registros
                ),
                2
            )


            # ----------------------------------------------
            # CÁLCULO DE HORAS EXTRA
            # ----------------------------------------------

            horas_extra = round(
                max(
                    0,
                    horas_totales
                    - LIMITE_HORAS_SEMANALES
                ),
                2
            )


            if registros:

                codigos_con_asistencia.add(
                    colaborador.codigo
                )


            nombre_corto = (
                colaborador.nombres[:22]
            )


            print(
                f"{colaborador.codigo:<8} "
                f"{nombre_corto:<22} "
                f"{dias_trabajados:>5} "
                f"{horas_totales:>9.2f} "
                f"{horas_extra:>10.2f}"
            )


        print(
            "========================================"
        )


        print(
            "Total colaboradores home office "
            "con registros: "
            f"{len(codigos_con_asistencia)}"
        )


        print(
            "Regla de horas extra: más de "
            f"{LIMITE_HORAS_SEMANALES} "
            "horas semanales"
        )


    # ======================================================
    # MENÚ PRINCIPAL
    # ======================================================

    def menu(self):

        while True:

            print(
                "\n=========================================="
            )

            print(
                "   SISTEMA DE ASISTENCIA HOME OFFICE"
            )

            print(
                "   Tottus - Área de Gestión de Procesos"
            )

            print(
                "=========================================="
            )

            print(
                "1. Registrar colaborador"
            )

            print(
                "2. Registrar asistencia"
            )

            print(
                "3. Listar todos los registros"
            )

            print(
                "4. Buscar por código de usuario"
            )

            print(
                "5. Editar registro de asistencia"
            )

            print(
                "6. Eliminar registro de asistencia"
            )

            print(
                "7. Ver resumen de cálculos"
            )

            print(
                "8. Salir"
            )

            print(
                "=========================================="
            )


            opcion = input(
                "Seleccione una opción: "
            ).strip()


            if opcion == "1":

                self.registrarColaborador()


            elif opcion == "2":

                self.registrarAsistencia()


            elif opcion == "3":

                self.listarAsistencias()


            elif opcion == "4":

                self.buscarAsistencia()


            elif opcion == "5":

                self.editarAsistencia()


            elif opcion == "6":

                self.eliminarAsistencia()


            elif opcion == "7":

                self.resumenCalculos()


            elif opcion == "8":

                print(
                    "\nSaliendo del sistema. "
                    "¡Hasta luego!"
                )

                break


            else:

                print(
                    "Opción inválida. "
                    "Intente nuevamente."
                )


# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# INTEGRACIÓN FINAL
# ==========================================================

if __name__ == "__main__":

    sistema = GestionAsistencia()

    sistema.menu()
         
