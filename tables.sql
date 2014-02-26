use salomon_1401;
drop table if exists Recursos,Actividades,Espacios,Horarios,Dependencias,Programas;

create table Dependencias (
    #PROPIEDADES
    dependencia tinyint,
    primary key (dependencia),

    nombre varchar(255),
    bloques varchar(255),

    #ENLACES
    programa_ids varchar(255)
);

create table Programas (
    #PROPIEDADES
    programa varchar(20) not null,
    primary key (programa),

    nombre varchar(255),

    #ENLACES
    dependencia_id tinyint
);

create table Espacios (

    #PROPIEDADES
    espacio varchar(5),
    primary key (espacio),
    
    bloque smallint,
    numero mediumint,

    #ENLACES
    dependencia_id smallint,
    recurso_id smallint,
    horario_ids varchar(255)
);

create table Recursos (

    #PROPIEDADES
    recurso varchar(20),
    primary key (recurso),
    
    capacidad smallint,
    salacomputo tinyint(1) not null default 0,
    labquim tinyint(1) not null default 0,
    proyfijo tinyint(1) not null default 0,
    proymovil tinyint(1) not null default 0,
    tv tinyint(1) not null default 0,
    pantalla tinyint(1) not null default 0,
    computador tinyint(1) not null default 0,
    laptop tinyint(1) not null default 0,
    extension tinyint(1) not null default 0,
    red tinyint(1) not null default 0,
    tabacrilico tinyint(1) not null default 0,
    tabtiza tinyint(1) not null default 0,
    tabvidrio tinyint(1) not null default 0,
    mesa tinyint(1) not null default 0,
    atril tinyint(1) not null default 0,
    torremul tinyint(1) not null default 0,
    parlantes tinyint(1) not null default 0,
    camara tinyint(1) not null default 0,
    aire tinyint(1) not null default 0,
    ventilador tinyint(1) not null default 0,
    sillas_moviles tinyint(1) not null default 0,
    opacas tinyint(1) not null default 0,
    cortinas tinyint(1) not null default 0,
    wifi tinyint(1) not null default 0,
    windows tinyint(1) not null default 0,
    linux tinyint(1) not null default 0

);

create table Horarios (

    #PROPIEDADES
    horario varchar(20),
    primary key (horario),
    
    dia char,
    hora smallint,
    duracion smallint,
    eficiencia smallint,

    #ENLACES
    codigo_id varchar(20),
    espacio_id varchar(20)
);

create table Actividades (
    #PROPIEDADES
    codigo varchar(20),
    primary key (codigo),

    nombre varchar(255),
    grupo tinyint,
    matriculados mediumint,

    #ENLACES
    recurso_id mediumint,
    programa_id varchar(5),
    horario_ids varchar(255)
);

