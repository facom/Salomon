use salomon_1401;
drop table if exists Recursos,Actividades,Espacios,Horarios,Dependencias,Programas,Coincidencias;

create table Dependencias (
    #PROPIEDADES
    dependencia varchar(2),
    primary key (dependencia),

    nombre varchar(255),
    bloques varchar(255),

    #ENLACES
    programa_ids varchar(255) not null default ''
);

create table Programas (
    #PROPIEDADES
    programa varchar(3) not null,
    primary key (programa),

    nombre varchar(255) not null default '',

    #ENLACES
    dependencia_id varchar(2) not null default ''
);

create table Espacios (
    #PROPIEDADES
    espacio varchar(5),
    primary key (espacio),
    
    bloque varchar(2) not null default '',
    numero varchar(3) not null default '',

    #ENLACES
    dependencia_id varchar(2) not null default '',
    recurso_id varchar(50) not null default '',
    horario_ids varchar(1000) not null default ''
);

create table Recursos (

    #PROPIEDADES
    recurso varchar(50),
    primary key (recurso),
    
    capacidad varchar(10) not null default '',
    salacomputo varchar(10) not null default 0,
    aulalab varchar(10) not null default 0,
    proyfijo varchar(10) not null default 0,
    proymovil varchar(10) not null default 0,
    tv varchar(10) not null default 0,
    pantalla varchar(10) not null default 0,
    computador varchar(10) not null default 0,
    laptop varchar(10) not null default 0,
    extension varchar(10) not null default 0,
    red varchar(10) not null default 0,
    tabacrilico varchar(10) not null default 0,
    tabtiza varchar(10) not null default 0,
    tabvidrio varchar(10) not null default 0,
    mesa varchar(10) not null default 0,
    atril varchar(10) not null default 0,
    torremul varchar(10) not null default 0,
    parlantes varchar(10) not null default 0,
    camara varchar(10) not null default 0,
    aire varchar(10) not null default 0,
    ventilador varchar(10) not null default 0,
    sillas_moviles varchar(10) not null default 0,
    opacas varchar(10) not null default 0,
    cortinas varchar(10) not null default 0,
    wifi varchar(10) not null default 0,
    windows varchar(10) not null default 0,
    linux varchar(10) not null default 0
);

create table Horarios (
    #PROPIEDADES
    horario varchar(20),
    primary key (horario),
    
    dia varchar(2) not null default '',
    hora varchar(2) not null default '',
    duracion varchar(2) not null default '',

    eficiencia varchar(20) not null default '',
    puntaje varchar(20) not null default '',

    #ENLACES
    codigo_id varchar(20) not null default '',
    espacio_id varchar(20) not null default '',
    recurso_id varchar(50) not null default '',
    coincidencia_id varchar(50) not null default ''
);

create table Coincidencias (
    #PROPIEDADES
    coincidencia varchar(50),
    primary key (coincidencia),
       
    #ENLACES
    recurso_id varchar(50) not null default ''
);

create table Actividades (
    #PROPIEDADES
    codigo varchar(20),
    primary key (codigo),

    nombre varchar(255) not null default '',
    grupo varchar(2) not null default '',
    matriculados varchar(3) not null default '',

    #ENLACES
    programa_ids varchar(255) not null default '',
    horario_ids varchar(1000) not null default ''
);
