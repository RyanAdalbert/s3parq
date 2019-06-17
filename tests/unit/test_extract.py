# TODO: Modify some of these tests so that they can run on the new extract notebook

# import pytest
# from unittest.mock import patch
# from core.constants import ENVIRONMENT, ENV_BUCKET
# from core.helpers.configuration_mocker import ConfigurationMocker as CMock
# import core.models.configuration as C
# import core.contract as contract
# from core.transforms.shared.raw.extract import ExtractTransform
# import boto3
# import moto
# import time
# import tempfile
# import os
# import math

# def get_filename_from_path(file):
#     return os.path.split(file.name)[1]

# @moto.mock_s3
# def s3_setup():
#     client = boto3.client('s3')
#     n_time = time.time()
#     time_delta = 10000000
#     output_contract = contract.Contract(
#         branch='master', parent='bluth', child='cornballer', state='raw')
#     client.create_bucket(Bucket= ENV_BUCKET)

#     t_file_old = tempfile.NamedTemporaryFile()
#     t_file_old.write(b'Gobias some old coffee!')
#     file_name_old = get_filename_from_path(t_file_old)
#     contract_key = output_contract.get_key()
#     client.upload_file(Bucket=ENV_BUCKET, Filename= t_file_old.name, Key=contract_key+file_name_old
#         , ExtraArgs={"Metadata": {"source_modified_time": str(n_time - time_delta)}})

#     t_file_new = tempfile.NamedTemporaryFile()
#     t_file_new.write(b'Gobias some new coffee!')
#     file_name_new = get_filename_from_path(t_file_new)
#     client.upload_file(Bucket=ENV_BUCKET, Filename= t_file_new.name, Key=contract_key+file_name_new
#         , ExtraArgs={"Metadata": {"source_modified_time": str(n_time + time_delta)}})

#     return (t_file_old, t_file_new, output_contract, time_delta)


# @moto.mock_s3
# @patch.object(ExtractTransform,'_validate_required_params')
# def test_push_to_s3_updated_file(mock_validate):
#     mock_validate.return_value=True

#     t_file_old, t_file_new, output_contract, time_delta = s3_setup()
#     extract = ExtractTransform()
#     client = boto3.client('s3')
#     extract.push_to_s3(tmp_dir=os.path.dirname(t_file_old.name),
#                        output_contract=output_contract)
#     file_name = get_filename_from_path(t_file_old)
#     s3_time = float(client.head_object(Bucket=ENV_BUCKET, Key=output_contract.get_key()+file_name)[
#                     'Metadata']['source_modified_time'])

#     assert math.isclose(os.stat(t_file_old.name).st_mtime, s3_time, rel_tol=0.01)


# @moto.mock_s3
# @patch.object(ExtractTransform,'_validate_required_params')
# def test_push_to_s3_not_if_older(mock_validate):
#     mock_validate.return_value=True

#     t_file_old, t_file_new, output_contract, time_delta = s3_setup()
#     extract = ExtractTransform()
#     client = boto3.client('s3')
#     file_name_new = get_filename_from_path(t_file_new)
#     key = output_contract.get_key() + file_name_new

#     s3_time_before = float(client.head_object(
#         Bucket=ENV_BUCKET, Key=key)['Metadata']['source_modified_time'])
#     extract.push_to_s3(tmp_dir=os.path.dirname(t_file_new.name),
#                        output_contract=output_contract)

#     s3_time_after = float(client.head_object(
#         Bucket=ENV_BUCKET, Key=key)['Metadata']['source_modified_time'])

#     assert s3_time_after == s3_time_before


# @moto.mock_s3
# def test_file_needs_update_needs_update():
#     params = s3_setup()
#     extract = ExtractTransform()
#     check_update = extract._file_needs_update(
#         params[2], params[0].name, os.stat(params[0].name).st_mtime)
#     assert check_update is True


# @moto.mock_s3
# def test_file_needs_update_doesnt_need_update():
#     params = s3_setup()
#     extract = ExtractTransform()
#     check_update = extract._file_needs_update(params[2], params[1].name, 0)
#     assert check_update is False


# @moto.mock_s3
# def test_file_needs_update_doesnt_exist():
#     params = s3_setup()
#     extract = ExtractTransform()
#     t_file = tempfile.NamedTemporaryFile()
#     t_file.write(b'Gobias some coffee!')
#     check_update = extract._file_needs_update(
#         params[2], t_file, os.stat(t_file.name).st_mtime)
#     assert check_update is True


# def test_extract_validate_params_bad():
#     with pytest.raises(ValueError) as e:
#         extract = ExtractTransform()
#         extract._validate_required_params()

#     assert e.type == ValueError


# def test_extract_validate_params_good():
#     output_contract = contract.Contract(
#         branch='master', parent='bluth', child='cornballer',state='raw')
#     transformation = C.Transformation()
#     extract = ExtractTransform(output_contract=output_contract,transform=transformation)
#     extract._validate_required_params()


# def test_set_env_good():
#     extract =  ExtractTransform()

#     assert extract.env == ENVIRONMENT


# @patch("core.transforms.shared.raw.extract.ENVIRONMENT","Pretend-RSE")
# def test_set_env_bad():
#     with pytest.raises(ValueError) as e:
#         extract = ExtractTransform()
#         extract.set_env()

#     assert e.type == ValueError


# def test_set_output_contract():
#     output_contract = contract.Contract(
#         branch='master', parent='bluth', child='cornballer', state='raw')
#     extract = ExtractTransform()
#     extract.set_output_contract(output_contract)

#     assert output_contract == extract.output_contract


# def test_set_transform():
#     transformation = C.Transformation()
#     extract = ExtractTransform()
#     extract.set_transform(transformation)

#     assert transformation == extract.transform
