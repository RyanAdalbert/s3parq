from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
import core.models.configuration as config
from core.logging import LoggerMixin


class ConfigurationMocker(LoggerMixin):
    """ for development, creates in-memory database instance and a matching session and 
        gives you a bunch of mocked data.
        NOTE: This generates the models directly from the core.models.configuration.py model classes, 
        and could potentially differ from alembic migrations. 
    """

    def __init__(self)-> None:
        engine = config.GenerateEngine(in_memory=True).get_engine()

        # this instansiates the in-memory sqlite instance
        config.Base.metadata.create_all(engine)

        session = config.Session(engine)
        self.session = session.get_session()

    def get_session(self) -> Session:
        return self.session

    def generate_mocks(self)-> None:
        self._mock_administrators()
        self._mock_pharmaceutical_companies()
        self._mock_brands()
        self._mock_segments()
        self._mock_pipeline_types()
        self._mock_pipelines()
        self._mock_pipeline_state_types()
        self._mock_pipeline_states()
        self._mock_tags()
        self._mock_transformation_templates()
        self._mock_transformation_templates_tags()
        self._mock_transformations()
        self._mock_transformation_variables()

    def _mock_transformation_templates_tags(self)->None:
        self.logger.debug('Generating bridge table mocks for transformation_templates <=> tags.')
        t = config.TransformationTemplateTag
        self.session.add_all([
            t(transformation_template_id = 1, tag_id = 1),
            t(transformation_template_id = 2, tag_id = 1),
            t(transformation_template_id = 1, tag_id = 2),
            t(transformation_template_id = 1000, tag_id = 1)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_templates_tags mocks.')

    def _mock_tags(self)->None:
        self.logger.debug('Generating tag mocks.')
        t = config.Tag
        self.session.add_all([
            t(id=1, value = 'current'),
            t(id=2, value = 'deprecated'),
            t(id=3, value = 'beta')
        ])
        self.session.commit()
        self.logger.debug('Done generating tag mocks.')
    
    def _mock_administrators(self)->None:
        self.logger.debug('Generating administrator mocks.')
        a = config.Administrator
        self.session.add_all([
            a(id=1, first_name = "Fox", last_name = "Mulder", email_address="fwm@integrichain.com"),
            a(id=2, first_name = "Dana", last_name = "Skully", email_address="dks@integrichain.com"),
            a(id=3, first_name = "Alec", last_name="Wertheimer", email_address="ajw@integrichain.com"),
            a(id=4, first_name = "Natie", last_name="Bohnel", email_address="njb@integrichain.com")
        ])
        self.session.commit()
        self.logger.debug('Done generating administrator mocks.')
        
    def _mock_brands(self)-> None:
        self.logger.debug('Generating brand mocks.')
        b = config.Brand
        self.session.add_all([
            b(id=1, name="Teamocil", display_name="Teamocil", pharmaceutical_company_id=1),
            b(id=2, name="Cornballer", display_name="Corn Baller", pharmaceutical_company_id=2),
            b(id=3, name="ILUMYA", display_name="ILUMYA", pharmaceutical_company_id=3),
            b(id=4, name="ODOMZO", display_name="ODOMZO", pharmaceutical_company_id=3)])
        self.session.commit()
        self.logger.debug('Done generating brand mocks.')

    def _mock_pharmaceutical_companies(self)-> None:
        self.logger.debug('Generating pharmaceutical company mocks.')
        p = config.PharmaceuticalCompany
        self.session.add_all([
            p(id=1, display_name="Natural Life Food Company", name='Nfoods'),
            p(id=2, display_name="Sitwell Home Construction", name="Sitwell"),
            p(id=3, display_name="Stephanie", name="Stephanie")])
        self.session.commit()
        self.logger.debug('Done generating pharmaceutical company mocks.')

    def _mock_pipelines(self)-> None:
        self.logger.debug('Generating pipeline mocks.')
        p = config.Pipeline
        self.session.add_all([
            p(id=1, name="bluth_banana_regression", brand_id=2,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=2, name="bluth_profitability", brand_id=2,
              pipeline_type_id=2, run_frequency='hourly'),
            p(id=3, name="temocil_profitablility", brand_id=1,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=500, name="bluth_banana_regression_deprecated", brand_id=2,
              pipeline_type_id=1, is_active=False, run_frequency='hourly'),
            p(id=4, name="symphony_health_association_ilumya_extract", brand_id=3,
              pipeline_type_id=1, run_frequency='daily'),
            p(id=5, name="symphony_health_association_odomzo_extract", brand_id=4,
              pipeline_type_id=1, run_frequency='daily')])
        self.session.commit()
        self.logger.debug('Done generating pipeline mocks.')

    def _mock_pipeline_states(self)-> None:
        self.logger.debug('Generating pipeline state mocks.')
        p = config.PipelineState
        self.session.add_all([
            p(id=1, pipeline_state_type_id=1, pipeline_id=1, graph_order=0),
            p(id=2, pipeline_state_type_id=2, pipeline_id=1, graph_order=1),
            p(id=3, pipeline_state_type_id=3, pipeline_id=1, graph_order=2),
            p(id=4, pipeline_state_type_id=1, pipeline_id=2, graph_order=0),
            p(id=5, pipeline_state_type_id=1, pipeline_id=4, graph_order=0),
            p(id=6, pipeline_state_type_id=2, pipeline_id=4, graph_order=1),
            p(id=7, pipeline_state_type_id=3, pipeline_id=4, graph_order=2),
            p(id=8, pipeline_state_type_id=5, pipeline_id=4, graph_order=3),
            p(id=9, pipeline_state_type_id=7, pipeline_id=4, graph_order=4),
            p(id=10, pipeline_state_type_id=1, pipeline_id=5, graph_order=0),
            p(id=11, pipeline_state_type_id=2, pipeline_id=5, graph_order=1),
            p(id=12, pipeline_state_type_id=3, pipeline_id=5, graph_order=2),
            p(id=13, pipeline_state_type_id=5, pipeline_id=5, graph_order=3),
            p(id=14, pipeline_state_type_id=7, pipeline_id=5, graph_order=4)])
        self.session.commit()
        self.logger.debug('Done generating pipeline state mocks.')

    def _mock_pipeline_state_types(self)-> None:
        self.logger.debug('Generating pipeline state type mocks.')
        p = config.PipelineStateType
        self.session.add_all([
            p(id=1, name="raw"),
            p(id=2, name="ingest"),
            p(id=3, name="master"),
            p(id=4, name="enhance"),
            p(id=5, name="enrich"),
            p(id=6, name="metrics"),
            p(id=7, name="dimensional")])
        self.session.commit()
        self.logger.debug('Done generating pipeline state type mocks.')

    def _mock_pipeline_types(self)-> None:
        self.logger.debug('Generating pipeline type mocks.')
        p = config.PipelineType
        self.session.add_all([
            p(id=1, name="regression", segment_id=1),
            p(id=2, name="profitability", segment_id=2)])
        self.session.commit()
        self.logger.debug('Done generating pipeline type mocks.')

    def _mock_segments(self)-> None:
        self.logger.debug('Generating segment mocks.')
        s = config.Segment
        self.session.add_all([
            s(id=1, name="Patient"),
            s(id=2, name="Payer"),
            s(id=3, name="Distribution")])
        self.session.commit()
        self.logger.debug('Done generating segment mocks.')

    def _mock_transformations(self)-> None:
        self.logger.debug('Generating transformation mocks.')
        t = config.Transformation
        self.session.add_all([
            t(id=1, transformation_template_id=1,
              pipeline_state_id=1, graph_order=0),
            t(id=2, transformation_template_id=1,
              pipeline_state_id=5, graph_order=0),
            t(id=3, transformation_template_id=1,
              pipeline_state_id=2, graph_order=1),
            t(id=9, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=10, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=4, transformation_template_id=1,
              pipeline_state_id=4, graph_order=0),
            t(id=5, transformation_template_id=1,
              pipeline_state_id=4, graph_order=0),
            t(id=6, transformation_template_id=1,
              pipeline_state_id=4, graph_order=1),
            t(id=7, transformation_template_id=1,
              pipeline_state_id=4, graph_order=1),
            t(id=8, transformation_template_id=1,
              pipeline_state_id=4, graph_order=2),
            t(id=11, transformation_template_id=1,
              pipeline_state_id=2, graph_order=0),
            t(id=12, transformation_template_id=2,
              pipeline_state_id=1, graph_order=1),
            t(id=13, transformation_template_id=2,
              pipeline_state_id=2, graph_order=0),
            t(id=14, transformation_template_id=3, # ilumya - map product NDCs
              pipeline_state_id=7, graph_order=0),
            t(id=15, transformation_template_id=4, # infer med details
              pipeline_state_id=7, graph_order=2),
            t(id=16, transformation_template_id=5, # filter to brand
              pipeline_state_id=7, graph_order=1),
            t(id=17, transformation_template_id=6, # remap pharm codes
              pipeline_state_id=8, graph_order=0),
            t(id=18, transformation_template_id=7, # filter shipment only
              pipeline_state_id=8, graph_order=1),
            t(id=19, transformation_template_id=8, # extract column mapping
              pipeline_state_id=9, graph_order=0),
            t(id=20, transformation_template_id=3, # odomzo - map product NDCs
              pipeline_state_id=12, graph_order=0),
            t(id=21, transformation_template_id=4, # infer med details
              pipeline_state_id=12, graph_order=2),
            t(id=22, transformation_template_id=5, # filter to brand
              pipeline_state_id=12, graph_order=1),
            t(id=23, transformation_template_id=6, # remap pharm codes
              pipeline_state_id=13, graph_order=0),
            t(id=24, transformation_template_id=7, # filter shipment only
              pipeline_state_id=13, graph_order=1),
            t(id=25, transformation_template_id=8, # extract column mapping
              pipeline_state_id=14, graph_order=0),
            t(id=26, transformation_template_id=9, # final ingest transform (rayne) ilumya
              pipeline_state_id=6, graph_order=0),
            t(id=37, transformation_template_id=9,  # final ingest transform (rayne) ilumya
              pipeline_state_id=6, graph_order=0),
            t(id=38, transformation_template_id=9,  # final ingest transform (rayne) ilumya
              pipeline_state_id=6, graph_order=0),
            t(id=39, transformation_template_id=9,  # final ingest transform (rayne) ilumya
              pipeline_state_id=6, graph_order=0),
            t(id=40, transformation_template_id=9,  # final ingest transform (rayne) ilumya
              pipeline_state_id=6, graph_order=0),
            t(id=27, transformation_template_id=9, # final ingest transform (rayne) odomzo
              pipeline_state_id=11, graph_order=0),
            t(id=28, transformation_template_id=10, # publish to ftp ilumya
              pipeline_state_id=9, graph_order=1),
            t(id=29, transformation_template_id=10, # publish to ftp odomzo
              pipeline_state_id=14, graph_order=1),

            t(id=41, transformation_template_id=2, # publish to ftp odomzo
              pipeline_state_id=6, graph_order=1),
            t(id=1000, transformation_template_id=1000, pipeline_state_id=2, graph_order=2)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation mocks.')

    def _mock_transformation_templates(self)-> None:
        self.logger.debug('Generating transformation_template mocks.')
        tt = config.TransformationTemplate
        self.session.add_all([
            tt(id=1, name='extract_from_ftp',
                  variable_structures = ''' {"filesystem_path":{"datatype": "string", "description": "the remote path to the files"},
                          "secret_name":{"datatype":"string","description":"the name of the secret in secret manager"},
                          "prefix":{"datatype":"string","description":"the prefix of the files to get on the remote filesystem"},
                          "secret_type_of":{"datatype":"string","description":"the type of the remote server, used in the secret path"}
                          }''',
                          pipeline_state_type_id=1),
            tt(id=2, name='initial_ingest',
                variable_structures = ''' {"delimiter":{"datatype": "string", "description": "the input file delimiter"},
                "skip_rows":{"datatype":"int","description":"the number of rows to skip at the top of the file"},
                "encoding":{"datatype":"string","description":"the encoding of the input file"},
                "input_file_prefix":{"datatype":"string","description":"the prefix of the selected input files"}
                }''',
                pipeline_state_type_id=2),
            tt(id=3, name='symphony_health_association_map_product_ndcs',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"},
                "index_col":{"datatype":"string","description":"the index column to map NDCs in the source dataset (default is rx_ndc_number)"},
                "secret_name":{"datatype":"string","description":"the name of the secret in Secret Manager for platform2"},
                "secret_type_of":{"datatype":"string","description":"the type of the secret in Secret Manager for platform2"}
                }''',
                pipeline_state_type_id=3),    
            tt(id=4, name='symphony_health_association_infer_med_details',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"}}''',
                pipeline_state_type_id=3),
            tt(id=5, name='symphony_health_association_filter_to_brand',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"}}''',
                pipeline_state_type_id=3),
            tt(id=6, name='symphony_health_association_remap_pharm_codes',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"}}''',
                pipeline_state_type_id=5),
            tt(id=7, name='symphony_health_association_filter_shipment_only',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"}}''',
                pipeline_state_type_id=5),
            tt(id=8, name='symphony_health_association_extract_column_mapping',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "the name of the transform to input source data from"}}''',
                pipeline_state_type_id=7),
            tt(id=9, name='symphony_health_association_refinement',
                variable_structures=''' {"ingest_source_transform":{"datatype": "string", "description": "The input source transform"},
                "ingest_source_file_prefix":{"datatype":"string","description":"The input source file prefix"},
                "rec_date_col":{"datatype":"string","description":"The mapped dataset column"},
                "pharm_code_col":{"datatype":"string","description":"The mapped dataset column"},
                "pharm_npi":{"datatype":"string","description":"The mapped dataset column"},
                "transtype":{"datatype":"string","description":"The mapped dataset column"},
                "pharm_transaction_id":{"datatype":"string","description":"The mapped dataset column"},
                "trans_seq":{"datatype":"string","description":"The mapped dataset column"},
                "ref_source":{"datatype":"string","description":"The mapped dataset column"},
                "ref_date":{"datatype":"string","description":"The mapped dataset column"},
                "program_id":{"datatype":"string","description":"The mapped dataset column"},
                "pharmacy_id":{"datatype":"string","description":"The mapped dataset column"},
                "pat_last_name":{"datatype":"string","description":"The mapped dataset column"},
                "pat_first_name":{"datatype":"string","description":"The mapped dataset column"},
                "pat_dob":{"datatype":"string","description":"The mapped dataset column"},
                "pat_gender":{"datatype":"string","description":"The mapped dataset column"},
                "pat_addr1":{"datatype":"string","description":"The mapped dataset column"},
                "pat_addr2":{"datatype":"string","description":"The mapped dataset column"},
                "pat_city":{"datatype":"string","description":"The mapped dataset column"},
                "pat_state":{"datatype":"string","description":"The mapped dataset column"},
                "pat_zip":{"datatype":"string","description":"The mapped dataset column"},
                "dx1_code":{"datatype":"string","description":"The mapped dataset column"},
                "dx2_code":{"datatype":"string","description":"The mapped dataset column"},
                "status_date":{"datatype":"string","description":"The mapped dataset column"},
                "status_code":{"datatype":"string","description":"The mapped dataset column"},
                "sub_status":{"datatype":"string","description":"The mapped dataset column"},
                "pres_last_name":{"datatype":"string","description":"The mapped dataset column"},
                "pres_first_name":{"datatype":"string","description":"The mapped dataset column"},
                "pres_addr1":{"datatype":"string","description":"The mapped dataset column"},
                "pres_addr2":{"datatype":"string","description":"The mapped dataset column"},
                "pres_city":{"datatype":"string","description":"The mapped dataset column"},
                "pres_state":{"datatype":"string","description":"The mapped dataset column"},
                "pres_zip":{"datatype":"string","description":"The mapped dataset column"},
                "pres_phone":{"datatype":"string","description":"The mapped dataset column"},
                "pres_npi":{"datatype":"string","description":"The mapped dataset column"},
                "pres_dea":{"datatype":"string","description":"The mapped dataset column"},
                "facility_name":{"datatype":"string","description":"The mapped dataset column"},
                "rxdate":{"datatype":"string","description":"The mapped dataset column"},
                "rxnumber":{"datatype":"string","description":"The mapped dataset column"},
                "rxrefills":{"datatype":"string","description":"The mapped dataset column"},
                "rxfill":{"datatype":"string","description":"The mapped dataset column"},
                "refill_remaining":{"datatype":"string","description":"The mapped dataset column"},
                "prev_disp":{"datatype":"string","description":"The mapped dataset column"},
                "rx_ndc_number":{"datatype":"string","description":"The mapped dataset column"},
                "medication":{"datatype":"string","description":"The mapped dataset column"},
                "quantity":{"datatype":"string","description":"The mapped dataset column"},
                "day_supply":{"datatype":"string","description":"The mapped dataset column"},
                "ship_date":{"datatype":"string","description":"The mapped dataset column"},
                "ship_carrier":{"datatype":"string","description":"The mapped dataset column"},
                "shiptracking_num":{"datatype":"string","description":"The mapped dataset column"},
                "ship_location":{"datatype":"string","description":"The mapped dataset column"},
                "ship_address":{"datatype":"string","description":"The mapped dataset column"},
                "ship_city":{"datatype":"string","description":"The mapped dataset column"},
                "ship_state":{"datatype":"string","description":"The mapped dataset column"},
                "ship_zip":{"datatype":"string","description":"The mapped dataset column"},
                "has_medical":{"datatype":"string","description":"The mapped dataset column"},
                "primary_coverage_type":{"datatype":"string","description":"The mapped dataset column"},
                "primary_payer_name":{"datatype":"string","description":"The mapped dataset column"},
                "primary_payer_type":{"datatype":"string","description":"The mapped dataset column"},
                "secondary_coverage_type":{"datatype":"string","description":"The mapped dataset column"},
                "secondary_payer_name":{"datatype":"string","description":"The mapped dataset column"},
                "secondary_payer_type":{"datatype":"string","description":"The mapped dataset column"},
                "plan_paid_amt":{"datatype":"string","description":"The mapped dataset column"},
                "pat_copay":{"datatype":"string","description":"The mapped dataset column"},
                "copay_assist_amount":{"datatype":"string","description":"The mapped dataset column"},
                "oth_payer_amt":{"datatype":"string","description":"The mapped dataset column"},
                "xfer_pharmname":{"datatype":"string","description":"The mapped dataset column"},
                "msa_patient_id":{"datatype":"string","description":"The mapped dataset column"},
                "msa_patient_bmap":{"datatype":"string","description":"The mapped dataset column"},
                "metadata_run_timestamp":{"datatype":"string","description":"The mapped dataset column"},
                "metadata_app_version":{"datatype":"string","description":"The mapped dataset column"},
                "metadata_output_contract":{"datatype":"string","description":"The mapped dataset column"}}''',
                pipeline_state_type_id=2),
            tt(id=10, name='publish_to_ftp',
                variable_structures = ''' {"input_transform":{"datatype": "string", "description": "name of transformation to pull dataset from"},
                "prefix":{"datatype": "string", "description": "file prefix to publish to ftp"},
                "suffix":{"datatype":"string", "description":"file suffix to publish to ftp"},
                "filetype":{"datatype": "string", "description": "filetype to publish to ftp (DO NOT INCLUDE . IN FILETYPE)"},
                "separator":{"datatype": "string", "description": "single character separator for output file"},
                "compression":{"datatype": "int", "description": "if true, published file will be compressed as gzip"},
                "date_format":{"datatype": "string", "description": "string formatting for datetime"},
                "remote_path":{"datatype":"string", "description":"path to publish to on FTP server"},
                "secret_name":{"datatype":"string", "description":"the name of the secret in Secret Manager for FTP server"},
                "secret_type_of":{"datatype":"string", "description":"the type of the secret in Secret Manager for FTP server, almost always FTP"}
                }''',
                pipeline_state_type_id=7),
            tt(id=1000, name="hello_world",
                variable_structures = ''' {"noun":{"datatype":"string","description":"the thing we are saying hello to!"}}''',
                pipeline_state_type_id=2)
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_template mocks.')

    def _mock_transformation_variables(self)->None:
        self.logger.debug('Generating transformation_variables mocks')
        tv = config.TransformationVariable
        self.session.add_all([
            tv(id=5, name='filesystem_path', transformation_id=2, value='/upload/sha_dry_run_test_raw_fetch'),
            tv(id=6, name='prefix', transformation_id=2, value='INTEGRICHAIN_SUN_'),
            tv(id=1, name='secret_name', transformation_id=2, value='test-sftp'),
            tv(id=2, name='secret_type_of', transformation_id=2, value='FTP'),

            tv(id=3, name='filesystem_path', transformation_id=3, value='sudden_valley_holdings'),
            tv(id=4, name='secret_name', transformation_id=3, value='dev-sftp'),
            tv(id=12, name='prefix', transformation_id=3, value=''),
            tv(id=11, name='secret_type_of', transformation_id=3, value='FTP'),

            tv(id=7, name='filesystem_path', transformation_id=9, value=''),
            tv(id=8, name='prefix', transformation_id=9, value=''),
            tv(id=9, name='secret_name', transformation_id=9, value='dev-sftp'),
            tv(id=10, name='secret_type_of', transformation_id=9, value='FTP'),

            tv(id=13, name='filesystem_path', transformation_id=1, value='/incoming'),
            tv(id=14, name='prefix', transformation_id=1, value=''),
            tv(id=15, name='secret_name', transformation_id=1, value='dev-sftp'),
            tv(id=16, name='secret_type_of', transformation_id=1, value='FTP'),

            tv(id=17, name='filesystem_path', transformation_id=10, value='/incoming'),
            tv(id=18, name='prefix', transformation_id=10, value='test-extract-root-prefix'),
            tv(id=19, name='secret_name', transformation_id=10, value='dev-sftp'),
            tv(id=20, name='secret_type_of', transformation_id=10, value='FTP'),

            tv(id=21, name='filesystem_path', transformation_id=10, value='/incoming/testing_extract'),
            tv(id=22, name='prefix', transformation_id=11, value=''),
            tv(id=23, name='secret_name', transformation_id=11, value='dev-sftp'),
            tv(id=24, name='secret_type_of', transformation_id=11, value='FTP'),

            tv(id=25, name='delimiter', transformation_id=13, value='|'),
            tv(id=26, name='skip_rows', transformation_id=13, value=1),
            tv(id=27, name='encoding', transformation_id=13, value='iso8859'),
            tv(id=28, name='input_file_prefix', transformation_id=13, value='some-extracted-file'),

            tv(id=29, name="input_transform", transformation_id=14, value="symphony_health_association_refinement"),
            tv(id=30, name="index_col", transformation_id=14, value="rx_ndc_number"),
            tv(id=31, name="secret_name", transformation_id=14, value="platform2"),
            tv(id=32, name="secret_type_of", transformation_id=14, value="database"),

            tv(id=33, name="input_transform", transformation_id=15, value="symphony_health_association_filter_to_brand"),

            tv(id=34, name="input_transform", transformation_id=16, value="symphony_health_association_map_product_ndcs"),

            tv(id=35, name="input_transform", transformation_id=17, value="symphony_health_association_infer_med_details"),

            tv(id=36, name="input_transform", transformation_id=18, value="symphony_health_association_remap_pharm_codes"),

            tv(id=37, name="input_transform", transformation_id=19, value="symphony_health_association_filter_shipment_only"),

            tv(id=39, name="prefix", transformation_id=28, value="symphony_health_association"),
            tv(id=40, name="suffix", transformation_id=28, value=""),
            tv(id=41, name="remote_path", transformation_id=28, value="/upload/sha_dry_run_test_publish"),
            tv(id=42, name="secret_name", transformation_id=28, value="test-sftp"),
            tv(id=43, name="secret_type_of", transformation_id=28, value="FTP"),
            tv(id=439, name="input_transform", transformation_id=28, value="symphony_health_association_extract_column_mapping"),
            tv(id=440, name="separator", transformation_id=28, value="|"),
            tv(id=441, name="compression", transformation_id=28, value=False),
            tv(id=442, name="filetype", transformation_id=28, value="dat"),
            tv(id=443, name="date_format", transformation_id=28, value="%Y%m%d_%Y%m%d%H%M%S"),

            tv(id=438, name='delimiter', transformation_id=41, value='|'),
            tv(id=437, name='skip_rows', transformation_id=41, value=0),
            tv(id=436, name='encoding', transformation_id=41, value='iso8859'),
            tv(id=419, name='input_file_prefix',
               transformation_id=41, value='INTEGRICHAIN_SUN_ACCREDO_STATUSDISPENSE'),
            tv(id=420, name='delimiter', transformation_id=42, value='|'),
            tv(id=421, name='skip_rows', transformation_id=42, value=0),
            tv(id=422, name='encoding', transformation_id=42, value='iso8859'),
            tv(id=423, name='input_file_prefix',
               transformation_id=42, value='INTEGRICHAIN_SUN_BRIOVA_STATUSDISPENSE'),
            tv(id=424, name='delimiter', transformation_id=43, value='|'),
            tv(id=425, name='skip_rows', transformation_id=43, value=0),
            tv(id=426, name='encoding', transformation_id=43, value='iso8859'),
            tv(id=427, name='input_file_prefix',
               transformation_id=43, value='INTEGRICHAIN_SUN_CIGNA_STATUSDISPENSE'),
            tv(id=428, name='delimiter', transformation_id=44, value='|'),
            tv(id=429, name='skip_rows', transformation_id=44, value=0),
            tv(id=430, name='encoding', transformation_id=44, value='iso8859'),
            tv(id=431, name='input_file_prefix',
               transformation_id=44, value='INTEGRICHAIN_SUN_CVS_STATUSDISPENSE'),
            tv(id=432, name='delimiter', transformation_id=45, value='|'),
            tv(id=433, name='skip_rows', transformation_id=45, value=0),
            tv(id=434, name='encoding', transformation_id=45, value='iso8859'),
            tv(id=435, name='input_file_prefix',
               transformation_id=45, value='INTEGRICHAIN_SUN_WALGREENS_STATUSDISPENSE'),

            tv(id=59, name='ingest_source_transform', transformation_id=26, value="initial_ingest"),
            tv(id=60, name='ingest_source_file_prefix', transformation_id=26, value="INTEGRICHAIN_SUN_ACCREDO_STATUSDISPENSE"),
            tv(id=61, name='rec_date_col', transformation_id=26, value="Rec Date"),
            tv(id=62, name='pharm_code_col', transformation_id=26, value="Pharm Code"),
            tv(id=63, name='pharm_npi', transformation_id=26, value="Pharm NPI"),
            tv(id=64, name='transtype', transformation_id=26, value="transType"),
            tv(id=65, name='pharm_transaction_id', transformation_id=26, value="Pharm Transaction Id"),
            tv(id=66, name='trans_seq', transformation_id=26, value="Trans Seq"),
            tv(id=67, name='ref_source', transformation_id=26, value="Ref Source"),
            tv(id=68, name='ref_date', transformation_id=26, value="Ref Date"),
            tv(id=69, name='program_id', transformation_id=26, value="Program ID"),
            tv(id=70, name='pharmacy_id', transformation_id=26, value="Pharmacy ID"),
            tv(id=71, name='pat_last_name', transformation_id=26, value="Pat Last Name"),
            tv(id=72, name='pat_first_name', transformation_id=26, value="Pat First Name"),
            tv(id=73, name='pat_dob', transformation_id=26, value="Pat DOB"),
            tv(id=74, name='pat_gender', transformation_id=26, value="PatGender"),
            tv(id=75, name='pat_addr1', transformation_id=26, value="Pat Addr1"),
            tv(id=76, name='pat_addr2', transformation_id=26, value="Pat Addr2"),
            tv(id=77, name='pat_city', transformation_id=26, value="Pat City"),
            tv(id=78, name='pat_state', transformation_id=26, value="Pat State"),
            tv(id=79, name='pat_zip', transformation_id=26, value="Pat Zip"),
            tv(id=80, name='dx1_code', transformation_id=26, value="Dx1 Code"),
            tv(id=81, name='dx2_code', transformation_id=26, value="Dx2 Code"),
            tv(id=82, name='status_date', transformation_id=26, value="Status Date"),
            tv(id=83, name='status_code', transformation_id=26, value="Status Code"),
            tv(id=84, name='sub_status', transformation_id=26, value="Sub Status"),
            tv(id=85, name='pres_last_name', transformation_id=26, value="Pres Last Name"),
            tv(id=86, name='pres_first_name', transformation_id=26, value="Pres First Name"),
            tv(id=87, name='pres_addr1', transformation_id=26, value="Pres Addr1"),
            tv(id=88, name='pres_addr2', transformation_id=26, value="Pres Addr2"),
            tv(id=89, name='pres_city', transformation_id=26, value="Pres City"),
            tv(id=90, name='pres_state', transformation_id=26, value="Pres State"),
            tv(id=91, name='pres_zip', transformation_id=26, value="Pres Zip"),
            tv(id=92, name='pres_phone', transformation_id=26, value="Pres Phone"),
            tv(id=93, name='pres_npi', transformation_id=26, value="Pres NPI"),
            tv(id=94, name='pres_dea', transformation_id=26, value="Pres DEA"),
            tv(id=95, name='facility_name', transformation_id=26, value="Facility Name"),
            tv(id=96, name='rxdate', transformation_id=26, value="RxDate"),
            tv(id=97, name='rxnumber', transformation_id=26, value="RxNumber"),
            tv(id=98, name='rxrefills', transformation_id=26, value="RxRefills"),
            tv(id=99, name='rxfill', transformation_id=26, value="RxFill"),
            tv(id=100, name='refill_remaining', transformation_id=26, value="Refill Remaining"),
            tv(id=101, name='prev_disp', transformation_id=26, value="prev Disp"),
            tv(id=102, name='rx_ndc_number', transformation_id=26, value="Rx NDC Number"),
            tv(id=103, name='medication', transformation_id=26, value="Medication"),
            tv(id=104, name='quantity', transformation_id=26, value="Quantity"),
            tv(id=105, name='day_supply', transformation_id=26, value="Day Supply"),
            tv(id=106, name='ship_date', transformation_id=26, value="Ship Date"),
            tv(id=107, name='ship_carrier', transformation_id=26, value="Ship Carrier"),
            tv(id=108, name='shiptracking_num', transformation_id=26, value="shipTracking Num"),
            tv(id=109, name='ship_location', transformation_id=26, value="Ship Location"),
            tv(id=110, name='ship_address', transformation_id=26, value="Ship Address"),
            tv(id=111, name='ship_city', transformation_id=26, value="Ship City"),
            tv(id=112, name='ship_state', transformation_id=26, value="Ship State"),
            tv(id=113, name='ship_zip', transformation_id=26, value="Ship Zip"),
            tv(id=114, name='has_medical', transformation_id=26, value="Has Medical"),
            tv(id=115, name='primary_coverage_type', transformation_id=26, value="Primary CoverageType"),
            tv(id=116, name='primary_payer_name', transformation_id=26, value="Primary Payer Name"),
            tv(id=117, name='primary_payer_type', transformation_id=26, value="Primary Payer Type"),
            tv(id=118, name='secondary_coverage_type', transformation_id=26, value="Secondary CoverageType"),
            tv(id=119, name='secondary_payer_name', transformation_id=26, value="Secondary PayerName"),
            tv(id=120, name='secondary_payer_type', transformation_id=26, value="Secondary PayerType"),
            tv(id=121, name='plan_paid_amt', transformation_id=26, value="Plan Paid Amt"),
            tv(id=122, name='pat_copay', transformation_id=26, value="Pat Copay"),
            tv(id=123, name='copay_assist_amount', transformation_id=26, value="Copay Assist Amount"),
            tv(id=124, name='oth_payer_amt', transformation_id=26, value="Oth Payer Amt"),
            tv(id=125, name='xfer_pharmname', transformation_id=26, value="Xfer PharmName"),
            tv(id=126, name='msa_patient_id', transformation_id=26, value="MSA PATIENT ID"),
            tv(id=127, name='msa_patient_bmap', transformation_id=26, value="MSA PATIENT BMAP"),
            tv(id=404, name='metadata_run_timestamp', transformation_id=26, value="__metadata_run_timestamp"),
            tv(id=405, name='metadata_app_version', transformation_id=26, value="__metadata_app_version"),
            tv(id=406, name='metadata_output_contract', transformation_id=26, value="__metadata_output_contract"),

            tv(id=128, name='ingest_source_transform', transformation_id=37, value="initial_ingest"),
            tv(id=129, name='ingest_source_file_prefix', transformation_id=37, value="INTEGRICHAIN_SUN_BRIOVA_STATUSDISPENSE"),
            tv(id=130, name='rec_date_col', transformation_id=37, value="Rec Date"),
            tv(id=131, name='pharm_code_col', transformation_id=37, value="Pharm Code"),
            tv(id=132, name='pharm_npi', transformation_id=37, value="Pharm NPI"),
            tv(id=133, name='transtype', transformation_id=37, value="transType"),
            tv(id=134, name='pharm_transaction_id', transformation_id=37, value="Pharm Transaction Id"),
            tv(id=135, name='trans_seq', transformation_id=37, value="Trans Seq"),
            tv(id=136, name='ref_source', transformation_id=37, value="Ref Source"),
            tv(id=137, name='ref_date', transformation_id=37, value="Ref Date"),
            tv(id=138, name='program_id', transformation_id=37, value="Program ID"),
            tv(id=139, name='pharmacy_id', transformation_id=37, value="Pharmacy ID"),
            tv(id=140, name='pat_last_name', transformation_id=37, value="Pat Last Name"),
            tv(id=141, name='pat_first_name', transformation_id=37, value="Pat First Name"),
            tv(id=142, name='pat_dob', transformation_id=37, value="Pat DOB"),
            tv(id=143, name='pat_gender', transformation_id=37, value="Pat Gender"),
            tv(id=144, name='pat_addr1', transformation_id=37, value="Pat Addr1"),
            tv(id=145, name='pat_addr2', transformation_id=37, value="Pat Addr2"),
            tv(id=146, name='pat_city', transformation_id=37, value="Pat City"),
            tv(id=147, name='pat_state', transformation_id=37, value="Pat State"),
            tv(id=148, name='pat_zip', transformation_id=37, value="Pat Zip"),
            tv(id=149, name='dx1_code', transformation_id=37, value="Dx1 Code"),
            tv(id=150, name='dx2_code', transformation_id=37, value="Dx2 Code"),
            tv(id=151, name='status_date', transformation_id=37, value="Status Date"),
            tv(id=152, name='status_code', transformation_id=37, value="Status Code"),
            tv(id=153, name='sub_status', transformation_id=37, value="Sub Status"),
            tv(id=154, name='pres_last_name', transformation_id=37, value="Pres Last Name"),
            tv(id=155, name='pres_first_name', transformation_id=37, value="Pres First Name"),
            tv(id=156, name='pres_addr1', transformation_id=37, value="Pres Addr1"),
            tv(id=157, name='pres_addr2', transformation_id=37, value="Pres Addr2"),
            tv(id=158, name='pres_city', transformation_id=37, value="Pres City"),
            tv(id=159, name='pres_state', transformation_id=37, value="Pres State"),
            tv(id=160, name='pres_zip', transformation_id=37, value="Pres Zip"),
            tv(id=161, name='pres_phone', transformation_id=37, value="Pres Phone"),
            tv(id=162, name='pres_npi', transformation_id=37, value="Pres NPI"),
            tv(id=163, name='pres_dea', transformation_id=37, value="Pres DEA"),
            tv(id=164, name='facility_name', transformation_id=37, value="Facility Name"),
            tv(id=165, name='rxdate', transformation_id=37, value="RxDate"),
            tv(id=166, name='rxnumber', transformation_id=37, value="RxNumber"),
            tv(id=167, name='rxrefills', transformation_id=37, value="RxRefills"),
            tv(id=168, name='rxfill', transformation_id=37, value="RxFill"),
            tv(id=169, name='refill_remaining', transformation_id=37, value="Refill Remaining"),
            tv(id=170, name='prev_disp', transformation_id=37, value="Prev Disp"),
            tv(id=171, name='rx_ndc_number', transformation_id=37, value="Rx NDC Number"),
            tv(id=172, name='medication', transformation_id=37, value="Medication"),
            tv(id=173, name='quantity', transformation_id=37, value="Quantity"),
            tv(id=174, name='day_supply', transformation_id=37, value="Day Supply"),
            tv(id=175, name='ship_date', transformation_id=37, value="Ship Date"),
            tv(id=176, name='ship_carrier', transformation_id=37, value="Ship Carrier"),
            tv(id=177, name='shiptracking_num', transformation_id=37, value="ShipTracking Num"),
            tv(id=178, name='ship_location', transformation_id=37, value="Ship Location"),
            tv(id=179, name='ship_address', transformation_id=37, value="Ship Address"),
            tv(id=180, name='ship_city', transformation_id=37, value="Ship City"),
            tv(id=181, name='ship_state', transformation_id=37, value="Ship State"),
            tv(id=182, name='ship_zip', transformation_id=37, value="Ship Zip"),
            tv(id=183, name='has_medical', transformation_id=37, value="Has Medical"),
            tv(id=184, name='primary_coverage_type', transformation_id=37, value="Primary Coverage Type"),
            tv(id=185, name='primary_payer_name', transformation_id=37, value="Primary Payer Name"),
            tv(id=186, name='primary_payer_type', transformation_id=37, value="PrimaryPayer Type"),
            tv(id=187, name='secondary_coverage_type', transformation_id=37, value="Secondary Coverage Type"),
            tv(id=188, name='secondary_payer_name', transformation_id=37, value="Secondary Payer Name"),
            tv(id=189, name='secondary_payer_type', transformation_id=37, value="Secondary Payer Type"),
            tv(id=190, name='plan_paid_amt', transformation_id=37, value="Plan Paid Amt"),
            tv(id=191, name='pat_copay', transformation_id=37, value="Pat Copay"),
            tv(id=192, name='copay_assist_amount', transformation_id=37, value="Copay Assist Amount"),
            tv(id=193, name='oth_payer_amt', transformation_id=37, value="Oth Payer Amt"),
            tv(id=194, name='xfer_pharmname', transformation_id=37, value="Xfer PharmName"),
            tv(id=195, name='msa_patient_id', transformation_id=37, value="MSA PATIENT ID"),
            tv(id=196, name='msa_patient_bmap', transformation_id=37, value="MSA PATIENT BMAP"),
            tv(id=407, name='metadata_run_timestamp', transformation_id=37, value="__metadata_run_timestamp"),
            tv(id=408, name='metadata_app_version', transformation_id=37, value="__metadata_app_version"),
            tv(id=409, name='metadata_output_contract', transformation_id=37, value="__metadata_output_contract"),

            tv(id=197, name='ingest_source_transform', transformation_id=38, value="initial_ingest"),
            tv(id=198, name='ingest_source_file_prefix', transformation_id=38, value="INTEGRICHAIN_SUN_CIGNA_STATUSDISPENSE"),
            tv(id=199, name='rec_date_col', transformation_id=38, value="Rec Date"),
            tv(id=200, name='pharm_code_col', transformation_id=38, value="Pharm Code"),
            tv(id=201, name='pharm_npi', transformation_id=38, value="Pharm NPI"),
            tv(id=202, name='transtype', transformation_id=38, value="transType"),
            tv(id=203, name='pharm_transaction_id', transformation_id=38, value="Pharm Transaction Id"),
            tv(id=204, name='trans_seq', transformation_id=38, value="Trans Seq"),
            tv(id=205, name='ref_source', transformation_id=38, value="Ref Source"),
            tv(id=206, name='ref_date', transformation_id=38, value="Ref Date"),
            tv(id=207, name='program_id', transformation_id=38, value="Program ID"),
            tv(id=208, name='pharmacy_id', transformation_id=38, value="Pharmacy ID"),
            tv(id=209, name='pat_last_name', transformation_id=38, value="Pat Last Name"),
            tv(id=210, name='pat_first_name', transformation_id=38, value="Pat First Name"),
            tv(id=211, name='pat_dob', transformation_id=38, value="Pat DOB"),
            tv(id=212, name='pat_gender', transformation_id=38, value="Pat Gender"),
            tv(id=213, name='pat_addr1', transformation_id=38, value="Pat Addr1"),
            tv(id=214, name='pat_addr2', transformation_id=38, value="Pat Addr2"),
            tv(id=215, name='pat_city', transformation_id=38, value="Pat City"),
            tv(id=216, name='pat_state', transformation_id=38, value="Pat State"),
            tv(id=217, name='pat_zip', transformation_id=38, value="Pat Zip"),
            tv(id=218, name='dx1_code', transformation_id=38, value="Dx1 Code"),
            tv(id=219, name='dx2_code', transformation_id=38, value="Dx2 Code"),
            tv(id=220, name='status_date', transformation_id=38, value="Status Date"),
            tv(id=221, name='status_code', transformation_id=38, value="Status Code"),
            tv(id=222, name='sub_status', transformation_id=38, value="Sub Status"),
            tv(id=223, name='pres_last_name', transformation_id=38, value="Pres Last Name"),
            tv(id=224, name='pres_first_name', transformation_id=38, value="Pres First Name"),
            tv(id=225, name='pres_addr1', transformation_id=38, value="Pres Addr1"),
            tv(id=226, name='pres_addr2', transformation_id=38, value="Pres Addr2"),
            tv(id=227, name='pres_city', transformation_id=38, value="Pres City"),
            tv(id=228, name='pres_state', transformation_id=38, value="Pres State"),
            tv(id=229, name='pres_zip', transformation_id=38, value="Pres Zip"),
            tv(id=230, name='pres_phone', transformation_id=38, value="Pres Phone"),
            tv(id=231, name='pres_npi', transformation_id=38, value="Pres NPI"),
            tv(id=232, name='pres_dea', transformation_id=38, value="Pres DEA"),
            tv(id=233, name='facility_name', transformation_id=38, value="Facility Name"),
            tv(id=234, name='rxdate', transformation_id=38, value="RxDate"),
            tv(id=235, name='rxnumber', transformation_id=38, value="RxNumber"),
            tv(id=236, name='rxrefills', transformation_id=38, value="RxRefills"),
            tv(id=237, name='rxfill', transformation_id=38, value="RxFill"),
            tv(id=238, name='refill_remaining', transformation_id=38, value="Refill Remaining"),
            tv(id=239, name='prev_disp', transformation_id=38, value="prev Disp"),
            tv(id=240, name='rx_ndc_number', transformation_id=38, value="Rx NDC Number"),
            tv(id=241, name='medication', transformation_id=38, value="Medication"),
            tv(id=242, name='quantity', transformation_id=38, value="Quantity"),
            tv(id=243, name='day_supply', transformation_id=38, value="Day Supply"),
            tv(id=244, name='ship_date', transformation_id=38, value="Ship Date"),
            tv(id=245, name='ship_carrier', transformation_id=38, value="Ship Carrier"),
            tv(id=246, name='shiptracking_num', transformation_id=38, value="shipTracking Num"),
            tv(id=247, name='ship_location', transformation_id=38, value="Ship Location"),
            tv(id=248, name='ship_address', transformation_id=38, value="Ship Address"),
            tv(id=249, name='ship_city', transformation_id=38, value="Ship City"),
            tv(id=250, name='ship_state', transformation_id=38, value="Ship State"),
            tv(id=251, name='ship_zip', transformation_id=38, value="Ship Zip"),
            tv(id=252, name='has_medical', transformation_id=38, value="Has Medical"),
            tv(id=253, name='primary_coverage_type', transformation_id=38, value="Primary Coverage Type"),
            tv(id=254, name='primary_payer_name', transformation_id=38, value="Primary Payer Name"),
            tv(id=255, name='primary_payer_type', transformation_id=38, value="PrimaryPayer Type"),
            tv(id=256, name='secondary_coverage_type', transformation_id=38, value="Secondary Coverage Type"),
            tv(id=257, name='secondary_payer_name', transformation_id=38, value="Secondary Payer Name"),
            tv(id=258, name='secondary_payer_type', transformation_id=38, value="Secondary Payer Type"),
            tv(id=259, name='plan_paid_amt', transformation_id=38, value="Plan Paid Amt"),
            tv(id=260, name='pat_copay', transformation_id=38, value="Pat Copay"),
            tv(id=261, name='copay_assist_amount', transformation_id=38, value="Copay Assist Amount"),
            tv(id=262, name='oth_payer_amt', transformation_id=38, value="Oth Payer Amt"),
            tv(id=263, name='xfer_pharmname', transformation_id=38, value="Xfer PharmNameCA"),
            tv(id=264, name='msa_patient_id', transformation_id=38, value="MSA PATIENT ID"),
            tv(id=265, name='msa_patient_bmap', transformation_id=38, value="MSA PATIENT BMAP"),
            tv(id=410, name='metadata_run_timestamp', transformation_id=38, value="__metadata_run_timestamp"),
            tv(id=411, name='metadata_app_version', transformation_id=38, value="__metadata_app_version"),
            tv(id=412, name='metadata_output_contract', transformation_id=38, value="__metadata_output_contract"),

            tv(id=266, name='ingest_source_transform', transformation_id=39, value="initial_ingest"),
            tv(id=267, name='ingest_source_file_prefix', transformation_id=39, value="INTEGRICHAIN_SUN_CVS_STATUSDISPENSE"),
            tv(id=268, name='rec_date_col', transformation_id=39, value="Rec Date"),
            tv(id=269, name='pharm_code_col', transformation_id=39, value="Pharm Code"),
            tv(id=270, name='pharm_npi', transformation_id=39, value="Pharm NPI"),
            tv(id=271, name='transtype', transformation_id=39, value="trans Type"),
            tv(id=272, name='pharm_transaction_id', transformation_id=39, value="Pharm Transaction ID"),
            tv(id=273, name='trans_seq', transformation_id=39, value="Trans Seq"),
            tv(id=274, name='ref_source', transformation_id=39, value="Ref Source"),
            tv(id=275, name='ref_date', transformation_id=39, value="Ref Date"),
            tv(id=276, name='program_id', transformation_id=39, value="Program ID"),
            tv(id=277, name='pharmacy_id', transformation_id=39, value="Pharmacy ID"),
            tv(id=278, name='pat_last_name', transformation_id=39, value="Pat Last Name"),
            tv(id=279, name='pat_first_name', transformation_id=39, value="Pat First Name"),
            tv(id=280, name='pat_dob', transformation_id=39, value="Pat DOB"),
            tv(id=281, name='pat_gender', transformation_id=39, value="PatGender"),
            tv(id=282, name='pat_addr1', transformation_id=39, value="Pat Addr1"),
            tv(id=283, name='pat_addr2', transformation_id=39, value="Pat Addr2"),
            tv(id=284, name='pat_city', transformation_id=39, value="Pat City"),
            tv(id=285, name='pat_state', transformation_id=39, value="Pat State"),
            tv(id=286, name='pat_zip', transformation_id=39, value="Pat Zip"),
            tv(id=287, name='dx1_code', transformation_id=39, value="Dx1 Code"),
            tv(id=288, name='dx2_code', transformation_id=39, value="Dx2 Code"),
            tv(id=289, name='status_date', transformation_id=39, value="Status Date"),
            tv(id=290, name='status_code', transformation_id=39, value="Status Code"),
            tv(id=291, name='sub_status', transformation_id=39, value="Sub Status"),
            tv(id=292, name='pres_last_name', transformation_id=39, value="Pres Last Name"),
            tv(id=293, name='pres_first_name', transformation_id=39, value="Pres First Name"),
            tv(id=294, name='pres_addr1', transformation_id=39, value="Pres Addr1"),
            tv(id=295, name='pres_addr2', transformation_id=39, value="Pres Addr2"),
            tv(id=296, name='pres_city', transformation_id=39, value="Pres City"),
            tv(id=297, name='pres_state', transformation_id=39, value="Pres State"),
            tv(id=298, name='pres_zip', transformation_id=39, value="Pres Zip"),
            tv(id=299, name='pres_phone', transformation_id=39, value="Pres Phone"),
            tv(id=300, name='pres_npi', transformation_id=39, value="Pres NPI"),
            tv(id=301, name='pres_dea', transformation_id=39, value="Pres DEA"),
            tv(id=302, name='facility_name', transformation_id=39, value="Facility Name"),
            tv(id=303, name='rxdate', transformation_id=39, value="RxDate"),
            tv(id=304, name='rxnumber', transformation_id=39, value="RxNumber"),
            tv(id=305, name='rxrefills', transformation_id=39, value="RxRefills"),
            tv(id=306, name='rxfill', transformation_id=39, value="RxFill"),
            tv(id=307, name='refill_remaining', transformation_id=39, value="Refill Remaining"),
            tv(id=308, name='prev_disp', transformation_id=39, value="prev Disp"),
            tv(id=309, name='rx_ndc_number', transformation_id=39, value="Rx NDC Number"),
            tv(id=310, name='medication', transformation_id=39, value="Medication"),
            tv(id=311, name='quantity', transformation_id=39, value="Quantity"),
            tv(id=312, name='day_supply', transformation_id=39, value="Day Supply"),
            tv(id=313, name='ship_date', transformation_id=39, value="Ship Date"),
            tv(id=314, name='ship_carrier', transformation_id=39, value="Ship Carrier"),
            tv(id=315, name='shiptracking_num', transformation_id=39, value="shipTracking Num"),
            tv(id=316, name='ship_location', transformation_id=39, value="Ship Location"),
            tv(id=317, name='ship_address', transformation_id=39, value="Ship Address"),
            tv(id=318, name='ship_city', transformation_id=39, value="Ship City"),
            tv(id=319, name='ship_state', transformation_id=39, value="Ship State"),
            tv(id=320, name='ship_zip', transformation_id=39, value="Ship Zip"),
            tv(id=321, name='has_medical', transformation_id=39, value="Has Medical"),
            tv(id=322, name='primary_coverage_type', transformation_id=39, value="Primary Coverage Type"),
            tv(id=323, name='primary_payer_name', transformation_id=39, value="Primary Payer Name"),
            tv(id=324, name='primary_payer_type', transformation_id=39, value="Primary Payer Type"),
            tv(id=325, name='secondary_coverage_type', transformation_id=39, value="Secondary Coverage Type"),
            tv(id=326, name='secondary_payer_name', transformation_id=39, value="Secondary PayerName"),
            tv(id=327, name='secondary_payer_type', transformation_id=39, value="Secondary PayerType"),
            tv(id=328, name='plan_paid_amt', transformation_id=39, value="Plan Paid Amt"),
            tv(id=329, name='pat_copay', transformation_id=39, value="Pat Copay"),
            tv(id=330, name='copay_assist_amount', transformation_id=39, value="Copay Assist Amount"),
            tv(id=331, name='oth_payer_amt', transformation_id=39, value="Oth Payer Amt"),
            tv(id=332, name='xfer_pharmname', transformation_id=39, value="Xfer Pharm Name"),
            tv(id=333, name='msa_patient_id', transformation_id=39, value="MSA PATIENT ID"),
            tv(id=334, name='msa_patient_bmap', transformation_id=39, value="MSA PATIENT BMAP"),
            tv(id=413, name='metadata_run_timestamp', transformation_id=39, value="__metadata_run_timestamp"),
            tv(id=414, name='metadata_app_version', transformation_id=39, value="__metadata_app_version"),
            tv(id=415, name='metadata_output_contract', transformation_id=39, value="__metadata_output_contract"),

            tv(id=335, name='ingest_source_transform', transformation_id=40, value="initial_ingest"),
            tv(id=336, name='ingest_source_file_prefix', transformation_id=40, value="INTEGRICHAIN_SUN_WALGREENS_STATUSDISPENSE"),
            tv(id=337, name='rec_date_col', transformation_id=40, value="Rec Date"),
            tv(id=338, name='pharm_code_col', transformation_id=40, value="Pharm Code"),
            tv(id=339, name='pharm_npi', transformation_id=40, value="Pharm NPI"),
            tv(id=340, name='transtype', transformation_id=40, value="transType"),
            tv(id=341, name='pharm_transaction_id', transformation_id=40, value="Pharm Transaction Id"),
            tv(id=342, name='trans_seq', transformation_id=40, value="Trans Seq"),
            tv(id=343, name='ref_source', transformation_id=40, value="Ref Source"),
            tv(id=344, name='ref_date', transformation_id=40, value="Ref Date"),
            tv(id=345, name='program_id', transformation_id=40, value="Program ID"),
            tv(id=346, name='pharmacy_id', transformation_id=40, value="Pharmacy ID"),
            tv(id=347, name='pat_last_name', transformation_id=40, value="Pat Last Name"),
            tv(id=348, name='pat_first_name', transformation_id=40, value="Pat First Name"),
            tv(id=349, name='pat_dob', transformation_id=40, value="Pat DOB"),
            tv(id=350, name='pat_gender', transformation_id=40, value="PatGender"),
            tv(id=351, name='pat_addr1', transformation_id=40, value="Pat Addr1"),
            tv(id=352, name='pat_addr2', transformation_id=40, value="Pat Addr2"),
            tv(id=353, name='pat_city', transformation_id=40, value="Pat City"),
            tv(id=354, name='pat_state', transformation_id=40, value="Pat State"),
            tv(id=355, name='pat_zip', transformation_id=40, value="Pat Zip"),
            tv(id=356, name='dx1_code', transformation_id=40, value="Dx1 Code"),
            tv(id=357, name='dx2_code', transformation_id=40, value="Dx2 Code"),
            tv(id=358, name='status_date', transformation_id=40, value="Status Date"),
            tv(id=359, name='status_code', transformation_id=40, value="Status Code"),
            tv(id=360, name='sub_status', transformation_id=40, value="Sub Status"),
            tv(id=361, name='pres_last_name', transformation_id=40, value="Pres Last Name"),
            tv(id=362, name='pres_first_name', transformation_id=40, value="Pres First Name"),
            tv(id=363, name='pres_addr1', transformation_id=40, value="Pres Addr1"),
            tv(id=364, name='pres_addr2', transformation_id=40, value="Pres Addr2"),
            tv(id=365, name='pres_city', transformation_id=40, value="Pres City"),
            tv(id=366, name='pres_state', transformation_id=40, value="Pres State"),
            tv(id=367, name='pres_zip', transformation_id=40, value="Pres Zip"),
            tv(id=368, name='pres_phone', transformation_id=40, value="Pres Phone"),
            tv(id=369, name='pres_npi', transformation_id=40, value="Pres NPI"),
            tv(id=370, name='pres_dea', transformation_id=40, value="Pres DEA"),
            tv(id=371, name='facility_name', transformation_id=40, value="Facility Name"),
            tv(id=372, name='rxdate', transformation_id=40, value="RxDate"),
            tv(id=373, name='rxnumber', transformation_id=40, value="RxNumber"),
            tv(id=374, name='rxrefills', transformation_id=40, value="RxRefills"),
            tv(id=375, name='rxfill', transformation_id=40, value="RxFill"),
            tv(id=376, name='refill_remaining', transformation_id=40, value="Refill Remaining"),
            tv(id=377, name='prev_disp', transformation_id=40, value="prev Disp"),
            tv(id=378, name='rx_ndc_number', transformation_id=40, value="Rx NDC Number"),
            tv(id=379, name='medication', transformation_id=40, value="Medication"),
            tv(id=380, name='quantity', transformation_id=40, value="Quantity"),
            tv(id=381, name='day_supply', transformation_id=40, value="Day Supply"),
            tv(id=382, name='ship_date', transformation_id=40, value="Ship Date"),
            tv(id=383, name='ship_carrier', transformation_id=40, value="Ship Carrier"),
            tv(id=384, name='shiptracking_num', transformation_id=40, value="shipTracking Num"),
            tv(id=385, name='ship_location', transformation_id=40, value="Ship Location"),
            tv(id=386, name='ship_address', transformation_id=40, value="Ship Address"),
            tv(id=387, name='ship_city', transformation_id=40, value="Ship City"),
            tv(id=388, name='ship_state', transformation_id=40, value="Ship State"),
            tv(id=389, name='ship_zip', transformation_id=40, value="Ship Zip"),
            tv(id=390, name='has_medical', transformation_id=40, value="Has Medical"),
            tv(id=391, name='primary_coverage_type', transformation_id=40, value="Primary CoverageType"),
            tv(id=392, name='primary_payer_name', transformation_id=40, value="Primary Payer Name"),
            tv(id=393, name='primary_payer_type', transformation_id=40, value="Primary Payer Type"),
            tv(id=394, name='secondary_coverage_type', transformation_id=40, value="Secondary CoverageType"),
            tv(id=395, name='secondary_payer_name', transformation_id=40, value="Secondary PayerName"),
            tv(id=396, name='secondary_payer_type', transformation_id=40, value="Secondary PayerType"),
            tv(id=397, name='plan_paid_amt', transformation_id=40, value="Plan Paid Amt"),
            tv(id=398, name='pat_copay', transformation_id=40, value="Pat Copay"),
            tv(id=399, name='copay_assist_amount', transformation_id=40, value="Copay Assist Amount"),
            tv(id=400, name='oth_payer_amt', transformation_id=40, value="Oth Payer Amt"),
            tv(id=401, name='xfer_pharmname', transformation_id=40, value="Xfer PharmName"),
            tv(id=402, name='msa_patient_id', transformation_id=40, value="MSA PATIENT ID"),
            tv(id=403, name='msa_patient_bmap', transformation_id=40, value="MSA PATIENT BMAP"),
            tv(id=416, name='metadata_run_timestamp', transformation_id=40, value="__metadata_run_timestamp"),
            tv(id=417, name='metadata_app_version', transformation_id=40, value="__metadata_app_version"),
            tv(id=418, name='metadata_output_contract', transformation_id=40, value="__metadata_output_contract"),

            tv(id=1000, name="noun", transformation_id=1000, value="world")
        ])
        self.session.commit()
        self.logger.debug('Done generating transformation_variables mocks.')

def setup_base_session():
    mock = ConfigurationMocker()
    session = mock.get_session()
    session.add(PharmaceuticalCompany(id=1, display_name='test_client', name='test_client'))
    session.add(Brand(id=1, pharmaceutical_company_id=1, display_name='test_brand', name='test_brand'))
    session.add(Segment(id=1, name='test_segment'))
    session.add(PipelineType(id=1, segment_id=1, name='test_patient_pipeline'))
    session.add(Pipeline(id=1, pipeline_type_id=1, brand_id=1, name='test_pipeline'))
    return session
