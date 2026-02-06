import xml.etree.ElementTree as ET
from typing import List
from openpyxl.worksheet.worksheet import Worksheet
from .utils import strip_namespace, safe_text

SHEET_NAME = "ResTenants"

RES_TENANTS_COLUMNS: List[str] = [
    "Record_ID",
    "Source_ID",
    "Source_Code",
    "FirstName",
    "LastName",
    "MiddleName",
    "Salutation",
    "Address1",
    "Address2",
    "Address3",
    "Address4",
    "ExtraAddressLine",
    "City",
    "State",
    "ZipCode",
    "GovernmentId",
    "Gets1099",
    "Status",
    "PropertyId",
    "UnitId",
    "Rent",
    "LeaseFrom",
    "LeaseTo",
    "MoveIn",
    "MoveOut",
    "NoticeDate",
    "LastRenewalDate",
    "LeaseSignDate",
    "PaymentType",
    "PayableType",
    "AchOptOut",
    "Email",
    "Email2",
    "LateFeeMinimum",
    "LateFeePerDay",
    "LateFeeType",
    "LateFeeGraceDays",
    "LateFeePercent",
    "LateFeeGraceDays2",
    "LateFeeAmount2",
    "LateFeePercent2",
    "LateFeeMax",
    "LateFeeMaxPercent",
    "LateFeeMaxDays",
    "LateFeeAmountTypeMax",
    "LateFeeAmountType2",
    "LateFeeMinDue",
    "LeaseGrossSqft",
    "HasDepositAccounting",
    "MaintenanceNotes",
    "DueDay",
    "LateMonthDeposit",
    "DepositInterest",
    "LeaseDescription",
    "BedId",
    "IsBillToCustomer",
    "ApplicantId",
    "ReasonForMoveOut",
    "NsfCount",
    "LateFeeCount",
    "ProspectId",
    "IsMTM",
    "LeaseTerm",
    "NoticeType",
    "TotalCharges",
    "AffTenantType",
    "CancelMoveInDate",
    "NoticeResponsibilityDate",
    "DEPOSIT0",
    "DEPOSIT1",
    "DEPOSIT2",
    "DEPOSIT3",
    "DEPOSIT4",
    "DEPOSIT5",
    "DEPOSIT6",
    "DEPOSIT7",
    "DEPOSIT8",
    "DEPOSIT9",
    "PHONENUM0",
    "PHONENUM1",
    "PHONENUM2",
    "PHONENUM3",
    "PHONENUM4",
    "PHONENUM5",
    "PHONENUM6",
    "PHONENUM7",
    "PHONENUM8",
    "PHONENUM9",
    "IsEmployeeUnit",
    "BillToTenant",
    "MaintenanceBillTo",
    "OptForCRMEmails",
    "NonResident",
]


def export_restenants(xml_path: str, ws: Worksheet) -> None:
    """
    Writes one sheet:
      DataSection/ResTenants/ResTenant -> rows
    """
    ws.title = SHEET_NAME
    ws.append(RES_TENANTS_COLUMNS)

    # Stream parse; write a row when </ResTenant> closes
    for event, elem in ET.iterparse(xml_path, events=("end",)):
        if strip_namespace(elem.tag) == "ResTenant":
            row_map = {c: "" for c in RES_TENANTS_COLUMNS}

            for child in elem:
                key = strip_namespace(child.tag)
                if key in row_map:
                    row_map[key] = safe_text(child.text)

            ws.append([row_map[c] for c in RES_TENANTS_COLUMNS])
            elem.clear()
