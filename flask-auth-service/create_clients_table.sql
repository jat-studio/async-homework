-- Table: public.clients

-- DROP TABLE public.clients;

CREATE TABLE public.clients
(
    "Id" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "ClientSecret" character varying(256) COLLATE pg_catalog."default" NOT NULL,
    "Uuid" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "Email" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "FullName" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "Position" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    "IsActive" boolean NOT NULL,
    "Role" character varying(128) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT clients_pkey PRIMARY KEY ("Id")
)

TABLESPACE pg_default;

ALTER TABLE public.clients
    OWNER to oauth_service;

GRANT ALL ON TABLE public.clients TO oauth_service;