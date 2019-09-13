--
-- This file should be run in the event that a new configuration database is created
-- Generated from a PostgreSQL database dump
--

-- Dumped from database version 10.6
-- Dumped by pg_dump version 11.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: configuration_application; Type: DATABASE; Schema: -; Owner: configurator
--

CREATE DATABASE configuration_application WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE configuration_application OWNER TO configurator;

\connect configuration_application

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: auditing; Type: SCHEMA; Schema: -; Owner: configurator
--

CREATE SCHEMA auditing;


ALTER SCHEMA auditing OWNER TO configurator;

--
-- Name: SCHEMA auditing; Type: COMMENT; Schema: -; Owner: configurator
--

COMMENT ON SCHEMA auditing IS 'This schema is for recording changes to the rest of the database.';


--
-- Name: audit_events(); Type: FUNCTION; Schema: public; Owner: configurator
--

CREATE FUNCTION public.audit_events() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            IF TG_OP = 'INSERT'
            THEN 
            INSERT INTO auditing.events (table_name, actor, after_value)
            VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(NEW));
            RETURN NEW;

            ELSIF TG_OP = 'UPDATE'
            THEN
            INSERT INTO auditing.events (table_name, actor, before_value, after_value)
            VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(OLD), to_jsonb(NEW));
            RETURN NEW;
            
            ELSIF TG_OP = 'DELETE'
            THEN
                INSERT INTO auditing.events (table_name, actor, before_value)
                VALUES (TG_TABLE_NAME, NEW.last_actor, to_jsonb(OLD));
            RETURN NEW;
            END IF;
        END
        $$;


ALTER FUNCTION public.audit_events() OWNER TO configurator;

--
-- Name: create_table_comments(); Type: FUNCTION; Schema: public; Owner: configurator
--

CREATE FUNCTION public.create_table_comments() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
        DECLARE
            obj record;    
        BEGIN
          FOR obj IN SELECT * FROM pg_event_trigger_ddl_commands() WHERE command_tag in ('SELECT INTO','CREATE TABLE','CREATE TABLE AS')
          LOOP
            EXECUTE'
                    COMMENT ON COLUMN ' || obj.object_identity ||'.updated_at IS ''represents the most recent DML operation timestamp for a row.'';
                    COMMENT ON COLUMN ' || obj.object_identity ||'.created_at IS ''represents the timestamp a row was initially created.'';
                    COMMENT ON COLUMN ' || obj.object_identity ||'.last_actor IS ''represents the most recent user email to update or insert this row.'';
                 '; END LOOP;
        END;
        $$;


ALTER FUNCTION public.create_table_comments() OWNER TO configurator;

--
-- Name: FUNCTION create_table_comments(); Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON FUNCTION public.create_table_comments() IS 'applies common object comments to created_at, updated_at and last_actor columns.';


--
-- Name: trigger_updated_at_timestamp(); Type: FUNCTION; Schema: public; Owner: configurator
--

CREATE FUNCTION public.trigger_updated_at_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END
        $$;


ALTER FUNCTION public.trigger_updated_at_timestamp() OWNER TO configurator;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: events; Type: TABLE; Schema: auditing; Owner: configurator
--

CREATE TABLE auditing.events (
    id integer NOT NULL,
    table_name character varying,
    actor character varying,
    before_value jsonb,
    after_value jsonb,
    event_timestamp timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE auditing.events OWNER TO configurator;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: auditing; Owner: configurator
--

CREATE SEQUENCE auditing.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auditing.events_id_seq OWNER TO configurator;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: auditing; Owner: configurator
--

ALTER SEQUENCE auditing.events_id_seq OWNED BY auditing.events.id;


--
-- Name: administrators; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.administrators (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    email_address character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL
);


ALTER TABLE public.administrators OWNER TO configurator;

--
-- Name: COLUMN administrators.created_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.administrators.created_at IS 'represents the timestamp a row was initially created.';


--
-- Name: COLUMN administrators.updated_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.administrators.updated_at IS 'represents the most recent DML operation timestamp for a row.';


--
-- Name: COLUMN administrators.last_actor; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.administrators.last_actor IS 'represents the most recent user email to update or insert this row.';


--
-- Name: administrators_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.administrators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.administrators_id_seq OWNER TO configurator;

--
-- Name: administrators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.administrators_id_seq OWNED BY public.administrators.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO configurator;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.brands (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL,
    display_name character varying NOT NULL,
    pharmaceutical_company_id integer NOT NULL
);


ALTER TABLE public.brands OWNER TO configurator;

--
-- Name: TABLE brands; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.brands IS 'A single offering of a pharmaceutical company, most often a drug or medication.';


--
-- Name: brands_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.brands_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.brands_id_seq OWNER TO configurator;

--
-- Name: brands_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.brands_id_seq OWNED BY public.brands.id;


--
-- Name: pharmaceutical_companies; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.pharmaceutical_companies (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL,
    display_name character varying NOT NULL
);


ALTER TABLE public.pharmaceutical_companies OWNER TO configurator;

--
-- Name: TABLE pharmaceutical_companies; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.pharmaceutical_companies IS 'A single business acting as a client to IntegriChain.';


--
-- Name: pharmaceutical_companies_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.pharmaceutical_companies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pharmaceutical_companies_id_seq OWNER TO configurator;

--
-- Name: pharmaceutical_companies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.pharmaceutical_companies_id_seq OWNED BY public.pharmaceutical_companies.id;


--
-- Name: pipeline_state_types; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.pipeline_state_types (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.pipeline_state_types OWNER TO configurator;

--
-- Name: TABLE pipeline_state_types; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.pipeline_state_types IS 'An abstract grouping of pipeline states, one of: raw, ingest, master, enrich, enhance, metrics, dimensional.';


--
-- Name: COLUMN pipeline_state_types.name; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.pipeline_state_types.name IS 'One of raw, ingest, master, enhance, enrich, metrics, dimensional.';


--
-- Name: pipeline_state_types_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.pipeline_state_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pipeline_state_types_id_seq OWNER TO configurator;

--
-- Name: pipeline_state_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.pipeline_state_types_id_seq OWNED BY public.pipeline_state_types.id;


--
-- Name: pipeline_states; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.pipeline_states (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    pipeline_state_type_id integer NOT NULL,
    pipeline_id integer NOT NULL,
    graph_order integer NOT NULL
);


ALTER TABLE public.pipeline_states OWNER TO configurator;

--
-- Name: TABLE pipeline_states; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.pipeline_states IS 'A single instance of a pipeline state type comprised of ordered transform tasks.';


--
-- Name: COLUMN pipeline_states.graph_order; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.pipeline_states.graph_order IS 'The wave number of the pipeline state. States are executed in ascending numeric wave order, with equal wave values executing in parallel.';


--
-- Name: pipeline_states_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.pipeline_states_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pipeline_states_id_seq OWNER TO configurator;

--
-- Name: pipeline_states_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.pipeline_states_id_seq OWNED BY public.pipeline_states.id;


--
-- Name: pipeline_types; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.pipeline_types (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL,
    segment_id integer NOT NULL
);


ALTER TABLE public.pipeline_types OWNER TO configurator;

--
-- Name: TABLE pipeline_types; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.pipeline_types IS 'An abstract grouping of pipelines by similar purpose, ie edo, extract_only etc.';


--
-- Name: pipeline_types_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.pipeline_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pipeline_types_id_seq OWNER TO configurator;

--
-- Name: pipeline_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.pipeline_types_id_seq OWNED BY public.pipeline_types.id;


--
-- Name: pipelines; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.pipelines (
    is_active boolean DEFAULT false NOT NULL,
    description character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL,
    pipeline_type_id integer NOT NULL,
    brand_id integer NOT NULL,
    run_frequency character varying
);


ALTER TABLE public.pipelines OWNER TO configurator;

--
-- Name: TABLE pipelines; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.pipelines IS 'A single instance of a pipeline type comprised of ordered states.';


--
-- Name: COLUMN pipelines.run_frequency; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.pipelines.run_frequency IS 'The airflow-supported run frequency as a string (without the @ symbol). Expected values are weekly, monthly, hourly, daily, none, yearly. See https://airflow.apache.org/scheduler.html#dag-runs for more information.';


--
-- Name: pipelines_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.pipelines_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pipelines_id_seq OWNER TO configurator;

--
-- Name: pipelines_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.pipelines_id_seq OWNED BY public.pipelines.id;


--
-- Name: run_events; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.run_events (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone,
    last_actor character varying,
    id integer NOT NULL,
    pipeline_id integer NOT NULL
);


ALTER TABLE public.run_events OWNER TO configurator;

--
-- Name: COLUMN run_events.created_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.run_events.created_at IS 'represents the timestamp a row was initially created.';


--
-- Name: COLUMN run_events.updated_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.run_events.updated_at IS 'represents the most recent DML operation timestamp for a row.';


--
-- Name: COLUMN run_events.last_actor; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.run_events.last_actor IS 'represents the most recent user email to update or insert this row.';


--
-- Name: run_events_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.run_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.run_events_id_seq OWNER TO configurator;

--
-- Name: run_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.run_events_id_seq OWNED BY public.run_events.id;


--
-- Name: segments; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.segments (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.segments OWNER TO configurator;

--
-- Name: TABLE segments; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.segments IS 'The business unit within IntegriChain, one of patient, payer, or distribution.';


--
-- Name: COLUMN segments.name; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.segments.name IS 'The business divison of IntegriChain. Expected values are Distribution, Patient and Payer.';


--
-- Name: segments_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.segments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.segments_id_seq OWNER TO configurator;

--
-- Name: segments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.segments_id_seq OWNED BY public.segments.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.tags (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    value character varying NOT NULL
);


ALTER TABLE public.tags OWNER TO configurator;

--
-- Name: TABLE tags; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.tags IS 'A label used for grouping of other objects (non specific).';


--
-- Name: COLUMN tags.created_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.tags.created_at IS 'represents the timestamp a row was initially created.';


--
-- Name: COLUMN tags.updated_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.tags.updated_at IS 'represents the most recent DML operation timestamp for a row.';


--
-- Name: COLUMN tags.last_actor; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.tags.last_actor IS 'represents the most recent user email to update or insert this row.';


--
-- Name: COLUMN tags.value; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.tags.value IS 'The textual label of the tag ie current or beta etc.';


--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tags_id_seq OWNER TO configurator;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: transformation_templates; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.transformation_templates (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    name character varying NOT NULL,
    variable_structures character varying,
    pipeline_state_type_id integer
);


ALTER TABLE public.transformation_templates OWNER TO configurator;

--
-- Name: TABLE transformation_templates; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.transformation_templates IS 'An abstract group of transformations, usually 1:1 with a Jupyter Notebook, ie abc_unblind would be a transformation_template, abc_unblind_veritrol would be a transformation.';


--
-- Name: COLUMN transformation_templates.name; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformation_templates.name IS 'The human readable descriptive identifier of the transformation template.';


--
-- Name: COLUMN transformation_templates.pipeline_state_type_id; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformation_templates.pipeline_state_type_id IS 'The pipeline state that this transform is allowed to operate within.';


--
-- Name: transformation_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.transformation_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transformation_templates_id_seq OWNER TO configurator;

--
-- Name: transformation_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.transformation_templates_id_seq OWNED BY public.transformation_templates.id;


--
-- Name: transformation_templates_tags; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.transformation_templates_tags (
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    last_actor character varying,
    transformation_template_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.transformation_templates_tags OWNER TO configurator;

--
-- Name: TABLE transformation_templates_tags; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.transformation_templates_tags IS 'bridge table between transformation_templates and tags.';


--
-- Name: COLUMN transformation_templates_tags.created_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformation_templates_tags.created_at IS 'represents the timestamp a row was initially created.';


--
-- Name: COLUMN transformation_templates_tags.updated_at; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformation_templates_tags.updated_at IS 'represents the most recent DML operation timestamp for a row.';


--
-- Name: COLUMN transformation_templates_tags.last_actor; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformation_templates_tags.last_actor IS 'represents the most recent user email to update or insert this row.';


--
-- Name: transformation_variables; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.transformation_variables (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    transformation_id integer NOT NULL,
    name character varying NOT NULL,
    value character varying NOT NULL
);


ALTER TABLE public.transformation_variables OWNER TO configurator;

--
-- Name: TABLE transformation_variables; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.transformation_variables IS 'A value to be injected into the transformation at runtime. Variable names and convertable data types MUST match the variable_structures for the corresponding transformation_template.';


--
-- Name: transformation_variables_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.transformation_variables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transformation_variables_id_seq OWNER TO configurator;

--
-- Name: transformation_variables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.transformation_variables_id_seq OWNED BY public.transformation_variables.id;


--
-- Name: transformations; Type: TABLE; Schema: public; Owner: configurator
--

CREATE TABLE public.transformations (
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    last_actor character varying,
    id integer NOT NULL,
    transformation_template_id integer NOT NULL,
    pipeline_state_id integer NOT NULL,
    graph_order integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.transformations OWNER TO configurator;

--
-- Name: TABLE transformations; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON TABLE public.transformations IS 'A single instance of a transformation template, ie abc_unblind would be a transformation_template, abc_unblind_veritrol would be a transformation.';


--
-- Name: COLUMN transformations.graph_order; Type: COMMENT; Schema: public; Owner: configurator
--

COMMENT ON COLUMN public.transformations.graph_order IS 'The wave number of the transformation within a given pipeline state. Transforms are executed in ascending numeric wave order, with equal wave values executing in parallel.';


--
-- Name: transformations_id_seq; Type: SEQUENCE; Schema: public; Owner: configurator
--

CREATE SEQUENCE public.transformations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.transformations_id_seq OWNER TO configurator;

--
-- Name: transformations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: configurator
--

ALTER SEQUENCE public.transformations_id_seq OWNED BY public.transformations.id;


--
-- Name: events id; Type: DEFAULT; Schema: auditing; Owner: configurator
--

ALTER TABLE ONLY auditing.events ALTER COLUMN id SET DEFAULT nextval('auditing.events_id_seq'::regclass);


--
-- Name: administrators id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.administrators ALTER COLUMN id SET DEFAULT nextval('public.administrators_id_seq'::regclass);


--
-- Name: brands id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.brands ALTER COLUMN id SET DEFAULT nextval('public.brands_id_seq'::regclass);


--
-- Name: pharmaceutical_companies id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pharmaceutical_companies ALTER COLUMN id SET DEFAULT nextval('public.pharmaceutical_companies_id_seq'::regclass);


--
-- Name: pipeline_state_types id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_state_types ALTER COLUMN id SET DEFAULT nextval('public.pipeline_state_types_id_seq'::regclass);


--
-- Name: pipeline_states id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_states ALTER COLUMN id SET DEFAULT nextval('public.pipeline_states_id_seq'::regclass);


--
-- Name: pipeline_types id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_types ALTER COLUMN id SET DEFAULT nextval('public.pipeline_types_id_seq'::regclass);


--
-- Name: pipelines id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipelines ALTER COLUMN id SET DEFAULT nextval('public.pipelines_id_seq'::regclass);


--
-- Name: run_events id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.run_events ALTER COLUMN id SET DEFAULT nextval('public.run_events_id_seq'::regclass);


--
-- Name: segments id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.segments ALTER COLUMN id SET DEFAULT nextval('public.segments_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: transformation_templates id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_templates ALTER COLUMN id SET DEFAULT nextval('public.transformation_templates_id_seq'::regclass);


--
-- Name: transformation_variables id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_variables ALTER COLUMN id SET DEFAULT nextval('public.transformation_variables_id_seq'::regclass);


--
-- Name: transformations id; Type: DEFAULT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformations ALTER COLUMN id SET DEFAULT nextval('public.transformations_id_seq'::regclass);


--
-- Name: administrators administrators_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.administrators
    ADD CONSTRAINT administrators_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (id);


--
-- Name: pharmaceutical_companies pharmaceutical_companies_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pharmaceutical_companies
    ADD CONSTRAINT pharmaceutical_companies_pkey PRIMARY KEY (id);


--
-- Name: pipeline_state_types pipeline_state_types_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_state_types
    ADD CONSTRAINT pipeline_state_types_pkey PRIMARY KEY (id);


--
-- Name: pipeline_states pipeline_states_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_states
    ADD CONSTRAINT pipeline_states_pkey PRIMARY KEY (id);


--
-- Name: pipeline_types pipeline_types_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_types
    ADD CONSTRAINT pipeline_types_pkey PRIMARY KEY (id);


--
-- Name: pipelines pipelines_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipelines
    ADD CONSTRAINT pipelines_pkey PRIMARY KEY (id);


--
-- Name: run_events run_events_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.run_events
    ADD CONSTRAINT run_events_pkey PRIMARY KEY (id);


--
-- Name: segments segments_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.segments
    ADD CONSTRAINT segments_pkey PRIMARY KEY (id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: transformation_templates transformation_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_templates
    ADD CONSTRAINT transformation_templates_pkey PRIMARY KEY (id);


--
-- Name: transformation_templates_tags transformation_templates_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_templates_tags
    ADD CONSTRAINT transformation_templates_tags_pkey PRIMARY KEY (transformation_template_id, tag_id);


--
-- Name: transformation_variables transformation_variables_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_variables
    ADD CONSTRAINT transformation_variables_pkey PRIMARY KEY (id);


--
-- Name: transformations transformations_pkey; Type: CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformations
    ADD CONSTRAINT transformations_pkey PRIMARY KEY (id);


--
-- Name: brands brands_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER brands_audit AFTER INSERT OR DELETE OR UPDATE ON public.brands FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: brands brands_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER brands_updated_at BEFORE UPDATE ON public.brands FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: pharmaceutical_companies pharmaceutical_companies_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pharmaceutical_companies_audit AFTER INSERT OR DELETE OR UPDATE ON public.pharmaceutical_companies FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: pharmaceutical_companies pharmaceutical_companies_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pharmaceutical_companies_updated_at BEFORE UPDATE ON public.pharmaceutical_companies FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: pipeline_state_types pipeline_state_types_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_state_types_audit AFTER INSERT OR DELETE OR UPDATE ON public.pipeline_state_types FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: pipeline_state_types pipeline_state_types_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_state_types_updated_at BEFORE UPDATE ON public.pipeline_state_types FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: pipeline_states pipeline_states_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_states_audit AFTER INSERT OR DELETE OR UPDATE ON public.pipeline_states FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: pipeline_states pipeline_states_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_states_updated_at BEFORE UPDATE ON public.pipeline_states FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: pipeline_types pipeline_types_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_types_audit AFTER INSERT OR DELETE OR UPDATE ON public.pipeline_types FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: pipeline_types pipeline_types_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipeline_types_updated_at BEFORE UPDATE ON public.pipeline_types FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: pipelines pipelines_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipelines_audit AFTER INSERT OR DELETE OR UPDATE ON public.pipelines FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: pipelines pipelines_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER pipelines_updated_at BEFORE UPDATE ON public.pipelines FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: segments segments_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER segments_audit AFTER INSERT OR DELETE OR UPDATE ON public.segments FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: segments segments_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER segments_updated_at BEFORE UPDATE ON public.segments FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: transformation_templates transformation_templates_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformation_templates_audit AFTER INSERT OR DELETE OR UPDATE ON public.transformation_templates FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: transformation_templates transformation_templates_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformation_templates_updated_at BEFORE UPDATE ON public.transformation_templates FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: transformation_variables transformation_variables_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformation_variables_audit AFTER INSERT OR DELETE OR UPDATE ON public.transformation_variables FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: transformation_variables transformation_variables_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformation_variables_updated_at BEFORE UPDATE ON public.transformation_variables FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: transformations transformations_audit; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformations_audit AFTER INSERT OR DELETE OR UPDATE ON public.transformations FOR EACH ROW EXECUTE PROCEDURE public.audit_events();


--
-- Name: transformations transformations_updated_at; Type: TRIGGER; Schema: public; Owner: configurator
--

CREATE TRIGGER transformations_updated_at BEFORE UPDATE ON public.transformations FOR EACH ROW EXECUTE PROCEDURE public.trigger_updated_at_timestamp();


--
-- Name: brands brands_pharmaceutical_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pharmaceutical_company_id_fkey FOREIGN KEY (pharmaceutical_company_id) REFERENCES public.pharmaceutical_companies(id);


--
-- Name: pipeline_states pipeline_states_pipeline_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_states
    ADD CONSTRAINT pipeline_states_pipeline_id_fkey FOREIGN KEY (pipeline_id) REFERENCES public.pipelines(id);


--
-- Name: pipeline_states pipeline_states_pipeline_state_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_states
    ADD CONSTRAINT pipeline_states_pipeline_state_type_id_fkey FOREIGN KEY (pipeline_state_type_id) REFERENCES public.pipeline_state_types(id);


--
-- Name: pipeline_types pipeline_types_segment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipeline_types
    ADD CONSTRAINT pipeline_types_segment_id_fkey FOREIGN KEY (segment_id) REFERENCES public.segments(id);


--
-- Name: pipelines pipelines_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipelines
    ADD CONSTRAINT pipelines_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(id);


--
-- Name: pipelines pipelines_pipeline_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.pipelines
    ADD CONSTRAINT pipelines_pipeline_type_id_fkey FOREIGN KEY (pipeline_type_id) REFERENCES public.pipeline_types(id);


--
-- Name: run_events run_events_pipeline_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.run_events
    ADD CONSTRAINT run_events_pipeline_id_fkey FOREIGN KEY (pipeline_id) REFERENCES public.pipelines(id);


--
-- Name: transformation_templates_tags transformation_templates_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_templates_tags
    ADD CONSTRAINT transformation_templates_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: transformation_templates_tags transformation_templates_tags_transformation_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_templates_tags
    ADD CONSTRAINT transformation_templates_tags_transformation_template_id_fkey FOREIGN KEY (transformation_template_id) REFERENCES public.transformation_templates(id);


--
-- Name: transformation_variables transformation_variables_transformation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformation_variables
    ADD CONSTRAINT transformation_variables_transformation_id_fkey FOREIGN KEY (transformation_id) REFERENCES public.transformations(id);


--
-- Name: transformations transformations_pipeline_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformations
    ADD CONSTRAINT transformations_pipeline_state_id_fkey FOREIGN KEY (pipeline_state_id) REFERENCES public.pipeline_states(id);


--
-- Name: transformations transformations_transformation_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: configurator
--

ALTER TABLE ONLY public.transformations
    ADD CONSTRAINT transformations_transformation_template_id_fkey FOREIGN KEY (transformation_template_id) REFERENCES public.transformation_templates(id);


--
-- Name: common_comments; Type: EVENT TRIGGER; Schema: -; Owner: rdsadmin
--

CREATE EVENT TRIGGER common_comments ON ddl_command_end
         WHEN TAG IN ('SELECT INTO', 'CREATE TABLE', 'CREATE TABLE AS')
   EXECUTE PROCEDURE public.create_table_comments();


ALTER EVENT TRIGGER common_comments OWNER TO rdsadmin;

--
-- PostgreSQL database dump complete
--

