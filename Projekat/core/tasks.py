from celery import shared_task
from django.core.files.base import ContentFile
from Projekat.core.smiles import calculateproperties, smiles3d

@shared_task
def add_test(x, y):
    return x + y

# rac svojstava na osnovu strukture(koristi smiles polje)
@shared_task
def calculatecompoundprops(id):
    from Projekat.core.models import Compound

    result = {
        'success': False,
        'id': id,
        'err': None
    }

    # uzima jedjinejnje
    try:
        compound = Compound.objects.get(id=id)
    except Compound.DoesNotExist:
        result['err'] = f"jed pod brojem {id} ne postoji"
        return result

    #provera za smiles
    if not compound.smiles:
        result['err'] = f"jed {compound.name} nema smiles"
        return result

    #iz smiles.py f-ja
    propsresult = calculateproperties(compound.smiles)

    if not propsresult['success']:
        result['err'] = propsresult['err']
        return result

    #  svojstva
    props = propsresult['properties']
    compound.logp = props.get('logp')
    compound.surface = props.get('surface')
    compound.h_donors = props.get('h_bond_donors')
    compound.h_acc = props.get('h_bond_acceptors')
    compound.calcproperties = True
    compound.save()

    result['success'] = True
    result['properties'] = {
        'logp': compound.logp,
        'surface': compound.surface,
        'h_donors': compound.h_donors,
        'h_acc': compound.h_acc,
    }
    return result

#generate3d je zasnovana na manuelnoj, ona koristi unete podatke, obradi ih pomocu man fje i prosledjuje je tako da je ona vec generisana u pozadini, dok smoiles3d generise tek kad korisnik zada tj kad klikne na details, tek se tada formira iz rdkit
# koristi online sajt za prikaz
@shared_task
def generatesmiles3d(id):
    from Projekat.core.models import Compound

    result = {
        'success': False,
        'id': id,
        'err': None
    }

    # uzima jedjinejnje
    try:
        compound = Compound.objects.get(id=id)
    except Compound.DoesNotExist:
        result['err'] = f"jed pod brojem {id} ne postoji"
        return result

    #provera za smiles
    if not compound.smiles:
        result['err'] = f"jed {compound.name} nema SMILES"
        return result

    #iz smiles.py f-ja
    pdb_result = smiles3d(compound.smiles)

    if not pdb_result['success']:
        result['err'] = pdb_result['err']
        return result

    # pdb fajl
    try:
        filename = f"{compound.name.replace(' ', '_')}_{compound.id}.pdb"
        compound.pdb.save(filename, ContentFile(pdb_result['pdb']))
        compound.structure = True
        compound.save()
    except Exception as err:
        result['err'] = str(err)
        return result

    result['success'] = True
    result['pdbfile'] = compound.pdb.url if compound.pdb else None
    return result