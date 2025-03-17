import config as config
from tabulate import tabulate


def calculate(taxable_amount, tax_rate) -> float:
    return taxable_amount * tax_rate

def get_deduction(tax_type) -> float:
    return config.TAX_DEDUCTION.get(tax_type)

def calculate_taxable_income(annual_income, tax_type) -> float:
    deductions = get_deduction(tax_type)
    return annual_income - deductions


def calculate_federal_income_tax(taxable_income) -> float:
    if taxable_income <= config.FED_CEILING_1:
        return calculate(taxable_income, config.FED_RATE_1)
    elif taxable_income <= config.FED_CEILING_2:
        return calculate(taxable_income-config.FED_CEILING_1, config.FED_RATE_2) + config.FED_OWED_2
    elif taxable_income <= config.FED_CEILING_3:
        return calculate(taxable_income-config.FED_CEILING_2, config.FED_RATE_3) + config.FED_OWED_3
    elif taxable_income <= config.FED_CEILING_4:
        return calculate(taxable_income-config.FED_CEILING_3, config.FED_RATE_4) + config.FED_OWED_4
    elif taxable_income <= config.FED_CEILING_5:
        return calculate(taxable_income-config.FED_CEILING_4, config.FED_RATE_5) + config.FED_OWED_5
    elif taxable_income <= config.FED_CEILING_6:
        return calculate(taxable_income-config.FED_CEILING_5, config.FED_RATE_6) + config.FED_OWED_6
    else:
        return calculate(taxable_income-config.FED_CEILING_6, config.FED_RATE_7) + config.FED_OWED_7


def calculate_state_income_tax(taxable_income) -> float:
    if taxable_income <= config.STATE_CEILING_1:
        return calculate(taxable_income, config.STATE_RATE_1)
    elif taxable_income <= config.STATE_CEILING_2:
        return calculate(taxable_income-config.STATE_CEILING_1, config.STATE_RATE_2) + config.STATE_OWED_2
    elif taxable_income <= config.STATE_CEILING_3:
        return calculate(taxable_income-config.STATE_CEILING_2, config.STATE_RATE_3) + config.STATE_OWED_3
    else:
        return calculate(taxable_income-config.STATE_CEILING_3, config.STATE_RATE_4) + config.STATE_OWED_4


def main() -> None:
    annual_income = config.COMPENSATION

    taxable_federal_income = calculate_taxable_income(annual_income, 'federal')
    federal_income_tax = calculate_federal_income_tax(taxable_federal_income)

    taxable_oasdi_income = calculate_taxable_income(annual_income, 'oasdi')
    oasdi_tax = calculate(taxable_oasdi_income, config.OASDI_RATE)

    taxable_medicare_income = calculate_taxable_income(annual_income, 'medicare')
    medicare_tax = calculate(taxable_medicare_income, config.MEDICARE_RATE)

    taxable_state_income = calculate_taxable_income(annual_income, 'state')
    income_tax_state = calculate_state_income_tax(taxable_state_income)

    total_taxes = federal_income_tax + oasdi_tax + medicare_tax + income_tax_state
    total_deductions = config.SUM_PRE_TAX_DEDUCTIONS+config.RETIREMENT_DEDUCTION

    print(tabulate([# ['Annual income', annual_income],
                    ['OASDI tax', oasdi_tax],
                    ['Medicare tax', medicare_tax],
                    ['Federal income tax', federal_income_tax],
                    ['State income tax', income_tax_state],
                    ['Total tax', total_taxes]],
                    floatfmt=".2f"))
    print(tabulate([['Annual income', annual_income],
                    ['Pre-tax deductions', total_deductions],
                    ['Total taxes', total_taxes],
                    ['Net income', annual_income - (total_taxes + total_deductions)]],
                    floatfmt=".2f"))

    # print(tabulate([# ['Monthly income', annual_income/26],
    #                 ['OASDI tax', oasdi_tax/26],
    #                 ['Medicare tax', medicare_tax/26],
    #                 ['Federal income tax', federal_income_tax/26],
    #                 ['State income tax', income_tax_state/26],
    #                 ['Total tax', (federal_income_tax+oasdi_tax+medicare_tax+income_tax_state)/26]],
    #                 floatfmt=".2f"))

if __name__ == "__main__":
    main()
