BASE_URL = "http://scp-wiki.net/"
SCP_ROUTE_TEMPLATE = "scp-{number:03d}"


def construct_url(scp_number):
    return BASE_URL + SCP_ROUTE_TEMPLATE.format(number=scp_number)
