use salomon;
drop table if exists recursos,actividades,espacios,horarios,dependencias,programas;

create table recursos (

    #PROPIEDADES
    recurso_id smallint not null AUTO_INCREMENT,
    primary key (recurso_id),
    
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
    parlantes tinyint(1) not null default 0,
    camara tinyint(1) not null default 0,
    sillas_moviles tinyint(1) not null default 0,
    opacas tinyint(1) not null default 0,
    cortinas tinyint(1) not null default 0,
    wifi tinyint(1) not null default 0,
    windows tinyint(1) not null default 0,
    linux tinyint(1) not null default 0,

    #ENLACES
    espacio_id smallint,
    actividad_id smallint
);

create table actividades (
    #PROPIEDADES
    actividad_id smallint not null AUTO_INCREMENT,
    primary key (actividad_id),

    nombre varchar(255),
    codigo varchar(255),

    #ENLACES
    recurso_id mediumint,
    dependencia_id smallint,
    programa_id smallint,
    horario_ids varchar(255)
);

create table espacios (

    #PROPIEDADES
    espacio_id mediumint not null  AUTO_INCREMENT,
    primary key (espacio_id),
    
    bloque smallint,
    numero smallint,
    capacidad smallint,

    #ENLACES
    horario_ids varchar(255),
    recurso_id smallint
);

create table horarios (

    #PROPIEDADES
    horario_id mediumint not null AUTO_INCREMENT,
    primary key (horario_id),
    
    dia char,
    hora smallint,
    duracion smallint,
    eficiencia smallint,

    #ENLACES
    actividad_id mediumint
);

create table dependencias (
    #PROPIEDADES
    dependencia_id tinyint not null AUTO_INCREMENT,
    primary key (dependencia_id),

    nombre varchar(255),
    bloques varchar(255),

    #ENLACES
    programa_ids varchar(255)
);

create table programas (
    #PROPIEDADES
    programa_id tinyint not null AUTO_INCREMENT,
    primary key (programa_id),

    nombre varchar(255),
    codigo varchar(255),

    #ENLACES
    dependencia_id tinyint
);

