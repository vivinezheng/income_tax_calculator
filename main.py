import config as config
from tabulate import tabulate


def calculate(taxable_amount, tax_rate) -> float:
    return taxable_amount * tax_rate


def federal_deductions(annual_income) -> float:
    return annual_income - sum(config.FEDERAL_DEDUCTIONS.values())


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


def state_deductions(annual_income) -> float:
    return annual_income - sum(config.STATE_DEDUCTIONS.values())


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
    annual_income=config.COMPENSATION
    federal_taxable_income=federal_deductions(annual_income=annual_income)
    federal_tax=calculate_federal_income_tax(federal_taxable_income)
    state_taxable_income=state_deductions(annual_income=annual_income)
    state_tax=calculate_state_income_tax(state_taxable_income)

    print(tabulate([['Annual income', annual_income],
                    ['Taxable federal income', federal_taxable_income],
                    ['Taxable state income', state_taxable_income],
                    ['Federal income tax', federal_tax],
                    ['State income tax', state_tax],
                    ['Total income tax', federal_tax + state_tax]],
                    floatfmt=".2f"))

if __name__ == "__main__":
    main()
