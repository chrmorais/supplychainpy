from decimal import Decimal

from supplychainpy.inventory.abc_xyz import AbcXyz

from supplychainpy import data_cleansing
from supplychainpy.inventory import economic_order_quantity
from supplychainpy.enum_formats import FileFormats
from supplychainpy.enum_formats import PeriodFormats
from supplychainpy.inventory import analyse_uncertain_demand


# TODO-feature retrieve data from csv based on column heading
def retrieve_data_from_csv():
    """ Retrieve data from csv with incorrect column arrangement.

    Retrieves data from csv with incorrect column arrangement, converting into analysis ready format. Columns must
    use similar naming convention and be in a uniform bucket (i.e. weeks, months quarters, days, year). The data cleaning module
    will use regex to identify columns for id, cost, price, quantity etc
    """
    pass


# TODO-feature specify length of orders, start position and period (day, week, month, ...)
# in the analysis function specify service-level expected for safety stock, a default is specified in the class
def analyse_orders(data_set: dict, sku_id: str, lead_time: Decimal, unit_cost: Decimal, reorder_cost: Decimal,
                   z_value: Decimal, retail_price: Decimal, quantity_on_hand: Decimal, currency:str ='USD') -> dict:
    """Analyse orders data for one sku using a dictionary.

    Analyses orders data for a single sku using the values in the data_set dict.

    Args:
        data_set (dict):        The orders data for a specified period.
        sku_id (str):           The unique id of the sku.
        lead_time (Decimal):    The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        unit_cost (Decimal):    The unit cost of the sku to the organisation.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock.
        retail_price (Decimal): The retail or standard price of the sku.
        quantity_on_hand (Decimal): The quantity currently on hand as of analysis or retrieving data set.

    Returns:
        dict:       The summary of the analysis, containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}

    Raises:
        ValueError: Dataset too small. Please use a minimum of 3 entries.


    Examples:

        yearly_demand = {'jan': 75, 'feb': 75, 'mar': 75, 'apr': 75, 'may': 75, 'jun': 75, 'jul': 25,
                      'aug': 25, 'sep': 25, 'oct': 25, 'nov': 25, 'dec': 25}

        summary = model_inventory.analyse_orders(yearly_demand,
                                         sku_id='RX983-90',
                                         lead_time=Decimal(3),
                                         unit_cost=Decimal(50.99),
                                         reorder_cost=Decimal(400),
                                         z_value=Decimal(1.28),
                                         retail_price=Decimal(600),
                                         quantity_on_hand=Decimal(390))
    """
    if len(data_set) > 2:
        d = analyse_uncertain_demand.UncertainDemand(orders=data_set, sku=sku_id, lead_time=lead_time,
                                                     unit_cost=unit_cost, reorder_cost=reorder_cost,
                                                     z_value=z_value, retail_price=retail_price,
                                                     quantity_on_hand=quantity_on_hand, currency=currency)
    else:
        raise ValueError("Dataset too small. Please use a minimum of 3 entries.")
    return d.orders_summary_simple()


def analyse_orders_from_file_col(file_path, sku_id: str, lead_time: Decimal, unit_cost: Decimal,
                                 reorder_cost: Decimal, z_value: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = PeriodFormats.months.name, currency='USD') -> dict:
    """Analyse orders from file arranged in a single column

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (file):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        sku_id (str):           The unique id of the sku.
        lead_time (Decimal):    The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        unit_cost (Decimal):    The unit cost of the sku to the organisation.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.
        retail_price (Decimal): The price at which the sku is retailed.


    Returns:
        dict:       The summary of the analysis, containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    Example:

    """

    if _check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            orders = data_cleansing.clean_orders_data_col_txt(f)
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            orders = data_cleansing.clean_orders_data_col_csv(f)
    else:
        raise Exception("Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.")
    f.close()
    d = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id, lead_time=lead_time,
                                                 unit_cost=unit_cost, reorder_cost=reorder_cost, z_value=z_value,
                                                 period=period, retail_price=retail_price, currency=currency)
    f.close()
    return d.orders_summary()


def analyse_orders_from_file_row(file_path: str, z_value: Decimal, reorder_cost: Decimal, retail_price: Decimal,
                                 file_type: str = FileFormats.text.name,
                                 period: str = "month", length: int = 12, currency: str ='USD') -> list:
    """Analyse multiple SKUs from a file with data arranged by row.

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (file):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        period (str):           The period of time the data points are bucketed into.

    Returns:
        list:       A list of summaries containing:
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    [{'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}, {'ABC_XYZ_Classification': 'AX',
                    'reorder_quantity': '258', 'revenue': '2090910.44', 'average_order': '539',
                    'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR481-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}]
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.


    """

    orders = {}
    analysed_orders_summary = []
    analysed_orders_collection = []

    if _check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            item_list = (data_cleansing.clean_orders_data_row(f, length=length))
            f.close()
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
            f.close()
    else:
        unspecified_file = "Unspecified file type, Please specify 'csv' or 'text' for file_type parameter."
        raise Exception(unspecified_file)
    # maybe use an iterable instead of unpacking for constructor
    try:
        for sku in item_list:
            sku_id = sku.get("sku id")
            unit_cost = sku.get("unit cost")
            lead_time = sku.get("lead time")

            quantity_on_hand = sku.get("quantity_on_hand")

            if quantity_on_hand == None:
                quantity_on_hand = 0.0
            orders['demand'] = sku.get("demand")

            analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders, sku=sku_id,
                                                                       lead_time=lead_time,
                                                                       unit_cost=unit_cost,
                                                                       reorder_cost=reorder_cost, z_value=z_value,
                                                                       retail_price=retail_price,
                                                                       quantity_on_hand=quantity_on_hand,
                                                                       currency=currency)

            analysed_orders_collection.append(analysed_orders)
            analysed_orders_summary.append(analysed_orders.orders_summary())
            orders = {}
            del analysed_orders
    except KeyError:
        print("The csv file is incorrectly formatted")
    return analysed_orders_summary


# TODO Remove hard coded holding cost and make it a parameter
def analyse_orders_abcxyz_from_file(file_path: str, z_value: Decimal, reorder_cost: Decimal,
                                    file_type: str = FileFormats.text.name,
                                    period: str = "month", length: int = 12, currency: str = 'USD') -> list:
    """Analyse orders data from file and returns ABCXYZ analysis

    Analyses orders data for a single sku, using the values from a file arranged in columns.The data should be arranged
    in two columns, 1 for the period and the other for the corresponding data-point.

    Args:
        file_path (str):       The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        reorder_cost (Decimal): The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        length (int):           The number of periods in the data-ser referenced from the second column of the row
                                onwards.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided by number
                                of purchase orders placed in the previous period.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):       Type of 'file csv' or 'text'
        period (str):          The period of time the data points are bucketed into.

    Returns:
        AbcXyz:     An AbcXyz class object is returned.
                    average_order,standard_deviation, safety_stock, demand_variability, reorder_level
                    reorder_quantity, revenue, economic_order_quantity, economic_order_variable_cost
                    and ABC_XYZ_Classification. For example:

                    {'ABC_XYZ_Classification': 'AX', 'reorder_quantity': '258', 'revenue': '2090910.44',
                    'average_order': '539', 'reorder_level': '813', 'economic_order_quantity': '277', 'sku': 'RR381-33',
                    'demand_variability': '0.052', 'economic_order_variable_cost': '29557.61',
                    'standard_deviation': '28', 'safety_stock': '51'}
    Raises:
        Exception:  Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter.
        Exception:  Unspecified file type, Please specify 'csv' or 'text' for file_type parameter.

    """

    analysed_orders_collection = []
    item_list = {}
    if _check_extension(file_path=file_path, file_type=file_type):
        if file_type == FileFormats.text.name:
            f = open(file_path, 'r')
            item_list = (data_cleansing.clean_orders_data_row(f, length))
        elif file_type == FileFormats.csv.name:
            f = open(file_path)
            item_list = data_cleansing.clean_orders_data_row_csv(f, length=length)
    else:
        incorrect_file = "Incorrect file type specified. Please specify 'csv' or 'text' for the file_type parameter."
        raise Exception(incorrect_file)

    for sku in item_list:
        orders = {}

        sku_id, unit_cost, lead_time, retail_price, quantity_on_hand = sku.get("sku id"), sku.get("unit cost"), sku.get(
            "lead time"), sku.get("retail_price"), sku.get("quantity_on_hand")

        orders['demand'] = sku.get("demand")
        total_orders = 0
        if quantity_on_hand == None:
            quantity_on_hand = 0.0
        for order in orders['demand']:
            total_orders += int(order)

        analysed_orders = analyse_uncertain_demand.UncertainDemand(orders=orders,
                                                                   sku=sku_id,
                                                                   lead_time=lead_time,
                                                                   unit_cost=unit_cost,
                                                                   reorder_cost=Decimal(reorder_cost),
                                                                   z_value=Decimal(z_value),
                                                                   retail_price=retail_price,
                                                                   quantity_on_hand=quantity_on_hand, currency=currency)

        average_orders = analysed_orders.average_orders

        reorder_quantity = analysed_orders.fixed_order_quantity

        eoq = economic_order_quantity.EconomicOrderQuantity(total_orders=float(total_orders),
                                                            reorder_quantity=float(reorder_quantity),
                                                            holding_cost=float(0.25),
                                                            reorder_cost=float(reorder_cost),
                                                            average_orders=average_orders,
                                                            unit_cost=float(unit_cost))

        analysed_orders.economic_order_qty = eoq.economic_order_quantity
        analysed_orders.economic_order_variable_cost = eoq.minimum_variable_cost

        analysed_orders_collection.append(analysed_orders)

    abc = AbcXyz(analysed_orders_collection)

    return analysed_orders_collection


# the np method allows a numpy array to be used. This requires the specification of a period and length the data is
# supposed to cover. This method also allows the use of lead time arrays for calculating average leadtimes. There
# also be an analyse_orders_from_file_np. using the analyse_orders_np method to process each row.

# def analyse_orders_np(unit_cost: Decimal, period: np.array, z_value: Decimal, orders: np.array,
#                      lead_time_np: np.array = [],
#                      lead_time: Decimal = 0.00, length: int = 12) -> dict:
#    d = analyse_uncertain_demand.UncertainDemandNp(orders_np=orders, length=length, period=period)
#    d.print_period()


def _check_extension(file_path, file_type: str) -> bool:
    """ Check the correct file type has been selected.

    Args:
        file_path (file):   The path to the file containing two columns of data, 1 period and 1 data-point for 1 sku.
        file_type (str):    specifying 'csv' or 'text'
    Returns:
        bool:

    """
    if file_path.endswith(".txt") and file_type.lower() == "text":
        flag = True
    elif file_path.endswith(".csv") and file_type.lower() == "csv":
        flag = True
    else:
        flag = False
    return flag

    # rewrite all of the to deal with database tables and rows instead of csv files.
