from dealers.models import Dealer
from individuals.models import Individual
from utils.sales import TransactionEntityType


def extract_id(data):
    return data.pop('id') if data.get('id') is not None else None


def fetch_individual(data):
    entity_id = extract_id(data)
    if entity_id:
        return Individual.objects.get(id=entity_id)

    return Individual.objects.filter(
        license_no=data.get('license_no'),
        dob=data.get('dob'),
        ssn_last_4=data.get('ssn_last_4'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
    ).first()


def fetch_dealer(data):
    entity_id = extract_id(data)
    if entity_id:
        return Dealer.objects.get(id=entity_id)
    return Dealer.objects.filter(
        ein=data.get('ein'),
        name=data.get('name'),
    ).first()


def fetch_or_create_dealer(data):
    dealer = fetch_dealer(data)
    if dealer:
        return dealer

    dealer = Dealer(ein=data.get('ein'), name=data.get('name'))
    dealer.save()
    return dealer

def fetch_or_create_individual(data):
    individual = fetch_individual(data)
    if individual:
        return individual

    individual = Individual(
        license_no=data.get('license_no'),
        dob=data.get('dob'),
        ssn_last_4=data.get('ssn_last_4'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
    )
    individual.save()
    return individual


TYPE_TO_ENTITY_FETCH = {
    TransactionEntityType.dealer.value: fetch_dealer,
    TransactionEntityType.individual.value: fetch_individual,
}


TYPE_TO_ENTITY_FETCH_OR_CREATE = {
    TransactionEntityType.dealer.value: fetch_or_create_dealer,
    TransactionEntityType.individual.value: fetch_or_create_individual,
}


def fetch_or_create_entity(data):
    entity_type = data.pop('type')
    return TYPE_TO_ENTITY_FETCH_OR_CREATE[entity_type](data)


def fetch_entity(data):
    entity_type = data.pop('type')
    return TYPE_TO_ENTITY_FETCH[entity_type](data)


def validate_buyer_seller_relationship(buyer, seller):
    if not buyer or not seller:
        return
    buyer_type = buyer.get('type')
    seller_type = seller.get('type')
    if seller_type == buyer_type:
        raise Exception('Buyer and Seller transactions '
            'cannot be created between two same type entities. '
            'Found buyer of type: {} and seller of type: {}'
            .format(buyer_type, seller_type))
