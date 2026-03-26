from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
#
#
# # smiles = 'CCO'
# #
# # mol  = Chem.MolFromSmiles(smiles)
# #
# # mol = Chem.AddHs(mol)
# #
# # AllChem.EmbedMolecule(mol, randomSeed=1)
# # AllChem.MMFFOptimizeMolecule(mol)
#
def smiles3d(smiles):
    result = {
        'success': False,
        'pdb': None,
        'err': None
    }

    if not smiles: #provera unosa polja
        result['err'] = 'smiles nije unesen'
        return result

    mol = Chem.MolFromSmiles(smiles) #kreiranje objekta iz str

    if mol is None: #provera formata
        result['err'] = 'Neispravan format'
        return result

    mol = Chem.AddHs(mol)
    status = AllChem.EmbedMolecule(mol)  #3d koord
    if status == -1:
        result['err'] = 'Neuspešno generisanje 3D strukture'
        return result

    AllChem.MMFFOptimizeMolecule(mol) #optimizacija geometr
    structure = Chem.MolToPDBBlock(mol) #generisanje strukture
    result['success'] = True
    result['pdb'] = structure
    return result

# funkcija za knverziju stringa smiles u 3d strukturu



def calculateproperties(smiles):
    result = {
        'success': False,
        'properties': None,
        'err': None
    }

    if not smiles: #provera unosa polja
        result['err'] = 'smiles nije unesen'
        return result

    mol = Chem.MolFromSmiles(smiles) #kreiranje objekta iz str

    if mol is None: #provera formata
        result['err'] = 'Neispravan format'
        return result

    #racunajnje svojstava
    try:
        logp = Descriptors.MolLogP(mol)
    except:
        logp = None

    try:
        surface = Descriptors.TPSA(mol)
    except:
        surface = None

    try:
        h_donors = Descriptors.NumHDonors(mol)
    except:
        h_donors = None

    try:
        h_acc = Descriptors.NumHAcceptors(mol)
    except:
        h_acc = None


#provera
    if logp is not None or surface is not None or h_donors is not None:
        result['success'] = True
        result['properties'] = {
            'logp': logp,
            'surface': surface,
            'h_bond_donors': h_donors,
            'h_bond_acceptors': h_acc,
        }

    else:
        result['err'] = 'grreska'

    return result


