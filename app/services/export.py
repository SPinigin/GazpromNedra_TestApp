import pandas as pd
from typing import List, Union
from io import BytesIO
from sqlalchemy.orm import Session
from app.models.license import License
from app.models.well import Well


class ExportService:
    @staticmethod
    def export_licenses_to_xls(licenses: List[License]) -> BytesIO:
        data = []
        for license in licenses:
            data.append({
                'ID': license.id,
                'Номер лицензии': license.number,
                'Дата выдачи': license.issue_date,
                'Срок действия': license.expire_date,
                'Предприятие': license.org.name,
                'ИНН': license.org.inn,
                'Статус': license.status.name,
                'Количество скважин': len(license.wells)
            })

            df = pd.DataFrame(data)

            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Лицензии', index=False)
            output.seek(0)

            return output

    @staticmethod
    def export_licenses_to_csv(licenses: List[License]) -> str:
        data = []
        for license in licenses:
            data.append({
                'ID': license.id,
                'Номер лицензии': license.number,
                'Дата выдачи': license.issue_date,
                'Срок действия': license.expiry_date,
                'Предприятие': license.company.name,
                'ИНН': license.company.inn,
                'Статус': license.status.name,
                'Количество скважин': len(license.wells)
            })

        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8')

    @staticmethod
    def export_wells_to_xls(wells: List[Well]) -> BytesIO:
        data = []
        for well in wells:
            data.append({
                'ID': well.id,
                'Название': well.number,
                'Глубина (м)': well.depth,
                'Дата бурения': well.drill_date,
                'Лицензия': well.license.number,
                'Предприятие': well.license.org.name,
                'Статус': well.status.name
            })

        df = pd.DataFrame(data)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Скважины', index=False)
        output.seek(0)

        return output

    @staticmethod
    def export_wells_to_csv(wells: List[Well]) -> str:
        data = []
        for well in wells:
            data.append({
                data.append({
                    'ID': well.id,
                    'Название': well.number,
                    'Глубина (м)': well.depth,
                    'Дата бурения': well.drill_date,
                    'Лицензия': well.license.number,
                    'Предприятие': well.license.org.name,
                    'Статус': well.status.name
                })
            })

        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8')

export_service = ExportService()