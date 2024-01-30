--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

-- Started on 2024-01-30 01:57:09 EET

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 218 (class 1259 OID 18507)
-- Name: Post; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Post" (
    id integer NOT NULL,
    title character varying NOT NULL,
    description text NOT NULL,
    placed_at timestamp without time zone DEFAULT now() NOT NULL,
    placed boolean NOT NULL,
    author_id integer NOT NULL,
    likes integer NOT NULL,
    dislikes integer NOT NULL
);


ALTER TABLE public."Post" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 18534)
-- Name: PostInteractions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PostInteractions" (
    id integer NOT NULL,
    is_like boolean NOT NULL,
    post_id integer NOT NULL,
    created_at date DEFAULT CURRENT_DATE NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public."PostInteractions" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 18533)
-- Name: PostInteractions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."PostInteractions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."PostInteractions_id_seq" OWNER TO postgres;

--
-- TOC entry 3640 (class 0 OID 0)
-- Dependencies: 221
-- Name: PostInteractions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."PostInteractions_id_seq" OWNED BY public."PostInteractions".id;


--
-- TOC entry 217 (class 1259 OID 18506)
-- Name: Post_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."Post_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."Post_id_seq" OWNER TO postgres;

--
-- TOC entry 3641 (class 0 OID 0)
-- Dependencies: 217
-- Name: Post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."Post_id_seq" OWNED BY public."Post".id;


--
-- TOC entry 216 (class 1259 OID 18492)
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    firstname character varying,
    lastname character varying,
    email character varying NOT NULL,
    "phoneNum" character varying,
    birthday date,
    username character varying NOT NULL,
    password character varying NOT NULL,
    subscribed_for_newsletter boolean NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 18491)
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."User_id_seq" OWNER TO postgres;

--
-- TOC entry 3642 (class 0 OID 0)
-- Dependencies: 215
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- TOC entry 214 (class 1259 OID 18486)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 18522)
-- Name: user_activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_activity (
    id integer NOT NULL,
    user_id integer NOT NULL,
    last_login timestamp without time zone,
    last_request timestamp without time zone
);


ALTER TABLE public.user_activity OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 18521)
-- Name: user_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_activity_id_seq OWNER TO postgres;

--
-- TOC entry 3643 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_activity_id_seq OWNED BY public.user_activity.id;


--
-- TOC entry 3459 (class 2604 OID 18510)
-- Name: Post id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Post" ALTER COLUMN id SET DEFAULT nextval('public."Post_id_seq"'::regclass);


--
-- TOC entry 3462 (class 2604 OID 18537)
-- Name: PostInteractions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PostInteractions" ALTER COLUMN id SET DEFAULT nextval('public."PostInteractions_id_seq"'::regclass);


--
-- TOC entry 3458 (class 2604 OID 18495)
-- Name: User id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- TOC entry 3461 (class 2604 OID 18525)
-- Name: user_activity id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_activity ALTER COLUMN id SET DEFAULT nextval('public.user_activity_id_seq'::regclass);


--
-- TOC entry 3630 (class 0 OID 18507)
-- Dependencies: 218
-- Data for Name: Post; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."Post" (id, title, description, placed_at, placed, author_id, likes, dislikes) FROM stdin;
1	string	string	2024-01-30 00:07:44.996283	t	2	0	1
2	string	string	2024-01-30 00:13:28.505165	t	2	0	0
\.


--
-- TOC entry 3634 (class 0 OID 18534)
-- Dependencies: 222
-- Data for Name: PostInteractions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."PostInteractions" (id, is_like, post_id, created_at, user_id) FROM stdin;
1	f	1	2024-01-30	2
\.


--
-- TOC entry 3628 (class 0 OID 18492)
-- Dependencies: 216
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."User" (id, firstname, lastname, email, "phoneNum", birthday, username, password, subscribed_for_newsletter) FROM stdin;
1	string	string	c92e97e1-5b0c-48ab-b46e-7737c4ff4ceb@example.com	03519e17-e6c9-4f93-92b3-c7b06e1ae00b	2010-01-25	80e59532-56e7-42db-b3e4-e2619ccea5be	$2b$12$BPMK7K.P34vZ0MSm4CEf/uVHE4igUnb.Wj3O0bGfr9BfP2xHyrJhi	f
2	string	string	110a3cd3-db87-46c7-b8f6-2b84acfd218a@example.com	0bb6bf01-b2d3-4356-bd62-f6cb3f770ece	2010-01-25	45134cf2-dea0-47b3-8daa-b352d1aae7a1	$2b$12$0lBeEy7fUKxEDnQqTwnAvuvUDYwO/ALZnIdgeKhMvsMKpiCV90o4m	f
3	string	string	910b4eff-c069-45c2-bb58-2a18ff72f124@example.com	f2f390f9-1a0d-4e57-914d-974eb29dd42f	2010-01-25	0202b096-1f6a-4bed-b36c-eb48b1020fe5	$2b$12$msIaBWvY1Lbn1rNqr4vUIe3.caMbSEA0EYB8FqFXQw5qSA3tUqOW.	f
4	string	string	5f0b807d-aef6-486e-aeaf-15de78627640@example.com	2db773f4-1375-4362-a0c3-bc420aa39c04	2010-01-25	69eda9cd-8acb-4412-ad39-1445f1cfe76b	$2b$12$4r86tDvd5fxCExbekHw3kOuyXL9ZakNDmdVInDif4DgUt7LQ4O.u.	f
\.


--
-- TOC entry 3626 (class 0 OID 18486)
-- Dependencies: 214
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
727348f0fcf4
\.


--
-- TOC entry 3632 (class 0 OID 18522)
-- Dependencies: 220
-- Data for Name: user_activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_activity (id, user_id, last_login, last_request) FROM stdin;
2	1	2024-01-30 00:08:34.30411	\N
1	2	\N	2024-01-30 00:13:31.125193
3	4	2024-01-30 00:13:53.007959	\N
\.


--
-- TOC entry 3644 (class 0 OID 0)
-- Dependencies: 221
-- Name: PostInteractions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."PostInteractions_id_seq"', 1, true);


--
-- TOC entry 3645 (class 0 OID 0)
-- Dependencies: 217
-- Name: Post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."Post_id_seq"', 2, true);


--
-- TOC entry 3646 (class 0 OID 0)
-- Dependencies: 215
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public."User_id_seq"', 4, true);


--
-- TOC entry 3647 (class 0 OID 0)
-- Dependencies: 219
-- Name: user_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_activity_id_seq', 3, true);


--
-- TOC entry 3479 (class 2606 OID 18540)
-- Name: PostInteractions PostInteractions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PostInteractions"
    ADD CONSTRAINT "PostInteractions_pkey" PRIMARY KEY (id);


--
-- TOC entry 3475 (class 2606 OID 18515)
-- Name: Post Post_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Post"
    ADD CONSTRAINT "Post_pkey" PRIMARY KEY (id);


--
-- TOC entry 3467 (class 2606 OID 18501)
-- Name: User User_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_email_key" UNIQUE (email);


--
-- TOC entry 3469 (class 2606 OID 18503)
-- Name: User User_phoneNum_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_phoneNum_key" UNIQUE ("phoneNum");


--
-- TOC entry 3471 (class 2606 OID 18499)
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 3473 (class 2606 OID 18505)
-- Name: User User_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- TOC entry 3465 (class 2606 OID 18490)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3477 (class 2606 OID 18527)
-- Name: user_activity user_activity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_pkey PRIMARY KEY (id);


--
-- TOC entry 3482 (class 2606 OID 18541)
-- Name: PostInteractions PostInteractions_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PostInteractions"
    ADD CONSTRAINT "PostInteractions_post_id_fkey" FOREIGN KEY (post_id) REFERENCES public."Post"(id);


--
-- TOC entry 3483 (class 2606 OID 18546)
-- Name: PostInteractions PostInteractions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PostInteractions"
    ADD CONSTRAINT "PostInteractions_user_id_fkey" FOREIGN KEY (user_id) REFERENCES public."User"(id);


--
-- TOC entry 3480 (class 2606 OID 18516)
-- Name: Post Post_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Post"
    ADD CONSTRAINT "Post_author_id_fkey" FOREIGN KEY (author_id) REFERENCES public."User"(id);


--
-- TOC entry 3481 (class 2606 OID 18528)
-- Name: user_activity user_activity_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_activity
    ADD CONSTRAINT user_activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."User"(id);


-- Completed on 2024-01-30 01:57:11 EET

--
-- PostgreSQL database dump complete
--

