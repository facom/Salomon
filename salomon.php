<?
$SCRIPTNAME=$_SERVER[SCRIPT_FILENAME];
$ROOTDIR=rtrim(shell_exec("dirname $SCRIPTNAME"));
require("$ROOTDIR/salomon-configuration.php");
//////////////////////////////////////////////////////////////
//CONECTA CON BASE DE DATOS
//////////////////////////////////////////////////////////////
$db=mysqli_connect("localhost",$USER,$PASSWORD,$DATABASE);

//////////////////////////////////////////////////////////////
//MAP TABLES<->PRIMARY 
//////////////////////////////////////////////////////////////
$sql="show tables;";
$out=mysqli_query($db,$sql);
$primaries=array();
while($row=mysqli_fetch_array($out)){
    $tabla=$row[0];
    $out2=mysqli_query($db,"show columns in $tabla;");
    while($fila=mysqli_fetch_array($out2)){
      if($fila[3]=="PRI"){
	$primary=$fila[0];
	break;
      }
    }
    $primaries[$primary]=$tabla;
}

//////////////////////////////////////////////////////////////
//TITULO
//////////////////////////////////////////////////////////////
echo "<h1>SALOMON</h1>";
echo "<h1>Facultad de Ciencias Exactas y Naturales</h1>";
echo "<h2><a href=?>Lista de Tablas</a></h2>";
echo "<h3>Ver tambien: <a href=salomon-reportes.php>Reportes</a>, <a href=salomon-acciones.php>Acciones</a></h2>";

if(false){
}else if($_GET["accion"]=="Navega"){
  //////////////////////////////////////////////////////////////
  //NAVEGA TABLA
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];
  $condicion=$_GET["condicion"];

  if("x$condicion"=="x"){
    $condsql="";
  }else{
    $condsql="where $condicion";
  }
  $sql="select * from $tabla $condsql;";

  echo "<h2>Tabla: $tabla</h2>";

echo<<<FILTRO
<form>
<input type="hidden" name="tabla" value="$tabla">
<input type="hidden" name="accion" value="Navega">
Filtro: <input type='text' name='condicion' value='$condicion'>
<input type="submit" name="accion" value="Navega">
<pre>
Ej. where puntaje>-100 order by cast(puntaje as signed int)
</pre>
</form>
<p></p>
<pre style="background:lightgray;padding:10px">$sql</pre>
<p></p>
FILTRO;

  echo "<table width=100% border=1px>";

  $out=mysqli_query($db,"show columns in $tabla;");
  echo "<tr><td>No.<a href='?accion=Nuevo&tabla=$tabla'>+</a></td>";
  $fields=array();
  while($row=mysqli_fetch_array($out)){
    $field=$row[0];
    array_push($fields,$field);
    echo "<td><b>$field</b></td>";
  }	
  echo "</tr>";

  $out=mysqli_query($db,$sql);
  $i=0;
  while($row=mysqli_fetch_array($out)){
    $id=$row[0];
    echo "<tr>";
    $i+=1;
    echo "<pre><td><a href='?accion=Edita&tabla=$tabla&campo=$fields[0]&id=$id'>$i</a></td></pre>";
    foreach($fields as $field){
      $value=$row[$field];
      if(preg_match("/_id$/",$field)){
	$parts=split("_",$field);
	$id=$parts[0];
	$tabla=$primaries[$id];
	$url="?accion=Navega&tabla=$tabla&condicion=$id%3D%27${value}%27";
	echo "<td><a href='$url'>$value</a></td>";
      }else if(preg_match("/_ids$/",$field)){
	$parts=split("_",$field);
	$id=$parts[0];
	$tabla=$primaries[$id];
	$values=split(";",$value);
	$valuestr="";
	foreach($values as $val){
	  if(!preg_match("/[\w\d]+/",$val)){continue;}
	  $url="?accion=Navega&tabla=$tabla&condicion=$id%3D%27${val}%27";
	  $valuestr.="<a href='$url'>$val</a>;";
	}
	echo "<td>$valuestr</td>";
      }else{
	echo "<td>$value</td>";
      }
    }
    echo "</tr>";
  }
  echo "</table>";

}else if($_GET["accion"]=="Buscar"){
  //////////////////////////////////////////////////////////////
  //BUSCAR
  //////////////////////////////////////////////////////////////
  $sql=$_GET["sql"];
echo<<<OUT
<pre style="background:lightgray;padding:10px">$sql</pre>
<p></p>
OUT;
 echo "<h2>Resultados</h2>";
 $out=mysqli_query($db,$sql);
 
 echo "<table width=100% border=1px>";
 $i=0;
 while($row=mysqli_fetch_array($out)){
   $id=$row[0];
   echo "<tr>";
   $i+=1;
   $numans=count($row);
   for($j=1;$j<$numans/2;$j++){
     $value=$row[$j];
     echo "<td>$value</td>";
   }
   echo "</tr>";
 }
 echo "</table>";
 
}else if($_GET["accion"]=="Edita"){
  //////////////////////////////////////////////////////////////
  //EDITAR
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];
  $campo=$_GET["campo"];
  $id=$_GET["id"];

  $out=mysqli_query($db,"show columns in $tabla;");
  $fields=array();
  while($row=mysqli_fetch_array($out)){
    $field=$row[0];
    array_push($fields,$field);
  }	
  $page=$_SERVER["HTTP_REFERER"];
  echo "<a href='$page'>Retornar</a>";
  echo "<form>";
  $sql="select * from $tabla where $campo='$id';";
  $out=mysqli_query($db,$sql);
  $row=mysqli_fetch_array($out);
  $i=0;
  foreach($fields as $field){
    $value=$row[$field];
    if($i==0){$opt="disabled";$idval=$value;}
    else{$opt="";}
    echo "$field: <input type='text' name='$field' value='$value' $opt><br/>";
    $i++;
  }
  echo "<input type='submit' name='accion' value='Actualiza'>";
  echo "<input type='submit' name='accion' value='Elimina'>";
  echo "<input type='hidden' name='tabla' value='$tabla'>";
  echo "<input type='hidden' name='page' value='$page'>";
  echo "<input type='hidden' name='id' value='$fields[0]'>";
  echo "<input type='hidden' name='idval' value='$idval'>";
  echo "</form>";

}else if($_GET["accion"]=="Actualiza"){
  //////////////////////////////////////////////////////////////
  //ACTUALIZAR
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];
  $page=$_GET["page"];
  $id=$_GET["id"];
  $idval=$_GET["idval"];

  $sql="update $tabla set ";
  foreach(array_keys($_GET) as $field){
    if($field=="tabla" or $field=="page" or $field=="accion" or $field=="id" or $field=="idval"){continue;}
    $value=$_GET[$field];
    $sql.="$field='$value',";
  }
  $sql=trim($sql,",");
  $sql.=" where $id='$idval';";
  echo "<pre style='background:lightgray;padding:10px'>$sql</pre>";
  if(!mysqli_query($db,$sql)){
    die("Error:".mysqli_error($db));
  }
  $referer=$_SERVER["HTTP_REFERER"];
  echo "<a href='$page'>Regresar a la Busqueda</a>, <a href='$referer'>Volver a editar</a>";

}else if($_GET["accion"]=="Nuevo"){
  //////////////////////////////////////////////////////////////
  //EDITAR
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];

  $out=mysqli_query($db,"show columns in $tabla;");
  $fields=array();
  while($row=mysqli_fetch_array($out)){
    $field=$row[0];
    array_push($fields,$field);
  }	

  $page=$_SERVER["HTTP_REFERER"];
  echo "<a href='$page'>Retornar</a>";
  echo "<form>";
  foreach($fields as $field){
    echo "$field: <input type='text' name='$field'><br/>";
    $i++;
  }
  echo "<input type='submit' name='accion' value='Agregar'>";
  echo "<input type='hidden' name='tabla' value='$tabla'>";
  echo "<input type='hidden' name='page' value='$page'>";
  echo "</form>";

 }else if($_GET["accion"]=="Agregar"){
  //////////////////////////////////////////////////////////////
  //AGREGAR
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];
  $page=$_GET["page"];

  $sql="insert into $tabla (";
  $out=mysqli_query($db,"show columns in $tabla;");
  $fields=array();
  while($row=mysqli_fetch_array($out)){
    $field=$row[0];
    $sql.="$field,";
    array_push($fields,$field);
  }	
  $sql=trim($sql,",");
  $sql.=") values (";

  foreach($fields as $field){
    $value=$_GET[$field];
    $sql.="'$value',";
  }
  $sql=trim($sql,",");
  $sql.=");";
  echo "<pre style='background:lightgray;padding:10px'>$sql</pre>";
  
  if(!mysqli_query($db,$sql)){
    die("Error:".mysqli_error($db));
  }
  echo "<a href='$page'>Regresar a la Busqueda</a>";

}else if($_GET["accion"]=="Elimina"){
  //////////////////////////////////////////////////////////////
  //ACTUALIZAR
  //////////////////////////////////////////////////////////////
  $tabla=$_GET["tabla"];
  $page=$_GET["page"];
  $id=$_GET["id"];
  $idval=$_GET["idval"];

  $sql="delete from $tabla where $id='$idval';";
  if(!mysqli_query($db,$sql)){
    die("Error:".mysqli_error($db));
  }
  echo "<pre style='background:lightgray;padding:10px'>$sql</pre>";
  echo "<a href='$page'>Regresar a la Busqueda</a>";
}else{
  //////////////////////////////////////////////////////////////
  //LISTA DE TABLAS
  //////////////////////////////////////////////////////////////
  echo "<h2>Tablas</h2>";
  $out=mysqli_query($db,"show tables;");
  echo "<ul>";
  while($row=mysqli_fetch_array($out)){
    $tabla=$row[0];
    $link="?accion=Navega&tabla=$tabla";
    echo "<li><a href=$link>$tabla</a></li>";
  }
  echo "</ul>";

  $notification="";
  if($_POST["accion"]=="Cargar"){
    if($_FILES["file"]["error"] > 0){
      echo "Error: " . $_FILES["file"]["error"] . "<br>";
    }else{
      $name=$_FILES["datafile"]["name"];
      $parts=preg_split("/\./",$name);
      $ext=$parts[1];
      $file=$_FILES["datafile"]["tmp_name"];
      if($ext!="zip"){
	shell_exec("cp -rf $file data/$name");
      }else{
	shell_exec("unzip $file -d data &> /tmp/err.log");
      }
      $notification="<p style='color:blue'>Carga de '$name' exitosa</p>";
    }
  }

  echo "<h2>Datos</h2>";
  $out=shell_exec("ls -ld data/*.csv");
  echo "<pre>$out</pre>";

echo<<<SQL
<form action="salomon.php" method="post" enctype="multipart/form-data">
  Cargar datos:<input type="file" name="datafile"><br/>
  <input type="submit" name="accion" value="Cargar">
</form>
$notification
SQL;

echo<<<SQL
<h2>Comando SQL</h2>
<form>
  SQL:<input type="text" name="sql" value="show tables;">
    <input type="submit" name="accion" value="Buscar">
</form>
SQL;
  
}
?>
<hr/>
<a href=mailto:zuluagajorge@gmail.com>Jorge I. Zuluaga</a> (CC) 2014
