from conftest import CONTRACT
import json


URLS = ['https://motion.example/a', 'https://motion.example/b', 'https://motion.example/c']


def opened(vm, deploy, owner):
    vm.strict_mocks = True; vm.check_pickling = True; vm.sender = owner
    contract = deploy(CONTRACT); contract.open_seal('seal-4', 'Four-corner motion loop', URLS)
    return contract


def sources(vm):
    vm.mock_web(r'/a$', {'status': 200, 'body': 'Rotate square 90 degrees clockwise.'})
    vm.mock_web(r'/b$', {'status': 200, 'body': 'Rotate square 180 degrees.'})
    vm.mock_web(r'/c$', {'status': 200, 'body': 'Rotate square 90 degrees clockwise.'})


def llm(vm, codes):
    vm.mock_llm(r'.*SymmetrySeal D4 extraction.*', json.dumps({'rows': [
        {'index': i, 'transform_code': code} for i, code in enumerate(codes)
    ]}))


def test_group_composition_closes(direct_vm, direct_deploy, direct_alice):
    contract = opened(direct_vm, direct_deploy, direct_alice); sources(direct_vm); llm(direct_vm, [1, 2, 1])
    contract.resolve_seal('seal-4'); row = contract.get_seal('seal-4')
    assert row['state'] == 'CLOSED' and row['composed_code'] == 0 and len(row['digests']) == 3


def test_non_identity_exposes_named_drift(direct_vm, direct_deploy, direct_alice):
    contract = opened(direct_vm, direct_deploy, direct_alice); sources(direct_vm); llm(direct_vm, [1, 1, 1])
    contract.resolve_seal('seal-4'); row = contract.get_seal('seal-4')
    assert row['state'] == 'DRIFT' and row['composed_name'] == 'ROTATE_270'


def test_reflection_composition(direct_vm, direct_deploy, direct_alice):
    contract = opened(direct_vm, direct_deploy, direct_alice); sources(direct_vm); llm(direct_vm, [4, 4, 0])
    contract.resolve_seal('seal-4'); assert contract.get_seal('seal-4')['state'] == 'CLOSED'


def test_validator_rejects_forged_transform(direct_vm, direct_deploy, direct_alice):
    contract = opened(direct_vm, direct_deploy, direct_alice); sources(direct_vm); llm(direct_vm, [1, 2, 1])
    result = contract._extract(contract.seals['SEAL-4']); assert direct_vm.run_validator(leader_result=result) is True
    forged = {'rows': [dict(item) for item in result['rows']], 'digests': result['digests']}; forged['rows'][0]['transform_code'] = 3
    assert direct_vm.run_validator(leader_result=forged) is False


def test_duplicate_id_and_source_rejected(direct_vm, direct_deploy, direct_alice):
    contract = opened(direct_vm, direct_deploy, direct_alice)
    with direct_vm.expect_revert('unique seal id'):
        contract.open_seal('seal-4', 'Duplicate seal', URLS)
    with direct_vm.expect_revert('distinct artifacts'):
        contract.open_seal('seal-5', 'Duplicate source', [URLS[0], URLS[0], URLS[2]])


def test_cancel_authorization_and_replay(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = opened(direct_vm, direct_deploy, direct_alice); direct_vm.sender = direct_bob
    with direct_vm.expect_revert('owner of open seal'):
        contract.cancel_open('seal-4')
    direct_vm.sender = direct_alice; sources(direct_vm); llm(direct_vm, [1, 2, 1]); contract.resolve_seal('seal-4')
    with direct_vm.expect_revert('open seal required'):
        contract.resolve_seal('seal-4')
