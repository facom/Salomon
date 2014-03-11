<?
$SCRIPTNAME=$_SERVER[SCRIPT_FILENAME];
$ROOTDIR=rtrim(shell_exec("dirname $SCRIPTNAME"));
require("$ROOTDIR/salomon-configuration.php");
//////////////////////////////////////////////////////////////
//CONECTA CON BASE DE DATOS
//////////////////////////////////////////////////////////////
$db=mysqli_connect("localhost","salomon","123","salomon_1401");

//////////////////////////////////////////////////////////////
//DATA
//////////////////////////////////////////////////////////////
$Days=array("L","M","W","J","V");
$Hours=array(6,8,10,12,14,16,18);

//////////////////////////////////////////////////////////////
//TITULO
//////////////////////////////////////////////////////////////
echo "<h1>SALOMON</h1>";
echo "<h1>Facultad de Ciencias Exactas y Naturales</h1>";
echo "<h2><a href=?>Reportes</a></h2>";
echo "<h3>Ver tambien: <a href=salomon.php>Lista de Tablas</a>, <a href=salomon-acciones.php>Acciones</a></h2>";

//////////////////////////////////////////////////////////////
//REPORTES
//////////////////////////////////////////////////////////////
if(false){
}else if(isset($_GET["HorarioAulas"])){

  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  //AULAS
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  $qespacio="";
  if(isset($_GET['espacio'])){
    $qespacio=$_GET['espacio'];
  }

  $sql="select espacio,horario_ids,recurso_id from Espacios";
  $out=mysqli_query($db,$sql);
  while($row=mysqli_fetch_array($out)){
    $espacio=$row[0];
    if($qespacio!="" and $espacio!=$qespacio){continue;}
    $horarioids=$row[1];
    $recursoid=$row[2];
    $rec=mysqli_query($db,"select capacidad from Recursos where recurso='$recursoid'");
    $result=mysqli_fetch_array($rec);
    $capacidad=$result[0];
    $horarioarr=split(";",$horarioids);
    echo "<h3><center>Aula <b>$espacio (Cap. $capacidad)</b></center></h3>";
    echo "<table border=1px width=100%>";
    echo "<tr><td width=2%><center><b>Hora</b></center></td>";
    foreach($Days as $day){
      echo "<td width=10%><b>$day</b></td>";
    }
    echo "</tr>";
    foreach($Hours as $hour){
      $h=sprintf("%02d",$hour);
      echo "<tr>";
      echo "<td><center><b>$h</b></center></td>";
      foreach($Days as $day){
	if(preg_match("/(\d+)-(\d)-$day-$hour/",$horarioids,$matches)){
	  $text="$matches[1] (Gr.$matches[2])";
	  $style="background-color:yellow";
	}else{
	  $text="";
	  $style="background:gray;";
	}
	echo "<td style=\"$style\">$text</td>";
      }
      echo "</tr>";
    }
    echo "</table>";
  }
}else if(isset($_GET["HorarioActividades"])){

  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  //ACTIVIDADES
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  $qcodigo="";
  if(isset($_GET['codigo'])){
    $qcodigo=$_GET['codigo'];
  }
  $sql="select codigo,nombre,horario_ids from Actividades";
  $out=mysqli_query($db,$sql);
  while($row=mysqli_fetch_array($out)){
    $codigo=$row[0];
    if($qcodigo!="" and $codigo!=$qcodigo){continue;}
    $nombre=$row[1];
    $horarioids=$row[2];

    $horarioarr=split(";",$horarioids);
    echo "<h3><center>Curso <b>$nombre ($codigo)</b></center></h3>";
    echo "<table border=1px width=100%>";
    echo "<tr><td width=2%><center><b>Hora</b></center></td>";
    foreach($Days as $day){
      echo "<td width=10%><b>$day</b></td>";
    }
    echo "</tr>";
    foreach($Hours as $hour){
      $h=sprintf("%02d",$hour);
      echo "<tr>";
      echo "<td><center><b>$h</b></center></td>";
      foreach($Days as $day){
	if(preg_match("/(\d+)-(\d)-$day-$hour-(\d+)/",$horarioids,$matches)){
	  $horarioid="$matches[1]-$matches[2]-$day-$hour-$matches[3]";

	  $rec=mysqli_query($db,"select recurso_id,eficiencia,puntaje from Horarios where horario='$horarioid'");
	  $result=mysqli_fetch_array($rec);
	  $recursoid=$result[0];
	  $eficiencia=round($result[1],1);
	  $puntaje=round($result[2],1);
	  
	  $rec=mysqli_query($db,"select capacidad from Recursos where recurso='$recursoid'");
	  $result=mysqli_fetch_array($rec);
	  $cupo=$result[0];
	  
	  $sql="select espacio_id from Horarios where horario='$horarioid'";
	  $out2=mysqli_query($db,$sql);
	  $result=mysqli_fetch_array($out2);
	  $espacio=$result[0];

	  $sql="select recurso_id from Espacios where espacio='$espacio'";
	  $out2=mysqli_query($db,$sql);
	  $result=mysqli_fetch_array($out2);
	  $recursoid=$result[0];
	  
	  $rec=mysqli_query($db,"select capacidad from Recursos where recurso='$recursoid'");
	  $result=mysqli_fetch_array($rec);
	  $capacidad=$result[0];

	  $urlact="salomon.php?tabla=Actividades&accion=Navega&condicion=codigo%3D%27$matches[1]%27&accion=Navega";
	  $urlact_rep="?HorarioActividades&codigo=$matches[1]";
	  $urlhor="salomon.php?tabla=Horarios&accion=Navega&condicion=horario%3D%27$horarioid%27&accion=Navega";
	  $urlhor_rep="?Coincidencias&horario=A$horarioid";
	  $urlesp="salomon.php?tabla=Espacios&accion=Navega&condicion=espacio%3D%27$espacio%27&accion=Navega";
	  $urlesp_rep="?HorarioAulas&espacio=$espacio";
	  $text=<<<TEXT
$matches[1]<sup><a href='$urlact' target='_blank'>db</a>|<a href='$urlact_rep' target='_blank'>rp</a></sup> 
(Gr. $matches[2]<sup><a href='$urlhor' target='_blank'>db</a>,<a href='$urlhor_rep' target='_blank'>cn</a></sup>
Cupo $cupo)<br/>
$espacio<sup><a href='$urlesp' target='_blank'>db</a>|<a href='$urlesp_rep' target='_blank'>rp</a></sup>(Cap. $capacidad)<br/>
Eff. $eficiencia, Scr. $puntaje
TEXT;
	  if($cupo<$capacidad){$color="yellow";}
	  else{$color="LightCoral";}
	  $style="background-color:$color";
	}else{
	  $text="";
	  $style="background:gray;";
	}
	echo "<td style=\"$style\">$text</td>";
      }
      echo "</tr>";
    }
    echo "</table>";
  }
}else if(isset($_GET["Coincidencias"])){
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  //READ COINCIDENCES
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  $table="";$header="";$content="";
  $out=mysqli_query($db,"show columns in Recursos;");
  $fields=array();
  $header.="<tr>";
  $count=array();
  while($row=mysqli_fetch_array($out)){
    $field=$row[0];
    array_push($fields,$field);
    $order=$field;
    if($field=="capacidad"){
      $order="cast($field as signed int)";
    }else if($field!="recurso"){
      $count[$field]=array("Vacio"=>0,
			   "Si"=>0,
			   "No"=>0,
			   "Sobrante"=>0);
    }
    if($field!="capacidad" and $field!="recurso"){
      $nlet=floor(strlen($field)/2);
      $fieldstr=substr($field,0,3).substr($field,$nlet,1);
    }else{$fieldstr=$field;}
    $header.="<td><a href='?Coincidencias&orderby=$order'>$fieldstr</a></td>";
  }	
  $header.="</tr>";
  $order="";
  if(isset($_GET["orderby"])){
    $ordfield=$_GET["orderby"];
    $order="order by $ordfield";
  }

  $qhorario="recurso like 'A%'";
  if(isset($_GET['horario'])){
    $qhorario="recurso='".$_GET['horario']."'";
  }
  
  $sql="select * from Recursos where $qhorario $order;";
  $out=mysqli_query($db,$sql);

  while($row=mysqli_fetch_array($out)){
    echo "<tr>";
    foreach($fields as $field){
      $value=$row[$field];
      $color="white";
      if($value=="Vacio"){
	$valuestr="";
	$count[$field]["Vacio"]++;
      }else if($value=="Si"){
	$color="green"; 
	$valuestr="";
	$count[$field]["Si"]++;
      }else if($value=="No"){
	$color="red";
	$valuestr="";
	$count[$field]["No"]++;
      }else if($value=="Sobrante"){
	$color="yellow";
	$valuestr="";
	$count[$field]["Sobrante"]++;
      }else{
	$valuestr=$value;
      }
      $prestr=""; 
      $poststr="";
      if($field=="recurso"){
	$value=preg_replace("/A/","",$valuestr);
	$urlhor="salomon.php?tabla=Horarios&accion=Navega&condicion=horario%3D%27$value%27&accion=Navega";
	$prestr="<a href='$urlhor' target='_blank'>";
	$poststr="</a>";
      }
      $content.="<td style='background:$color'>$prestr$valuestr$poststr</td>";
    }
    $content.="</tr>";
  }  
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  //REPORT
  //%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  $report="";
  $casos=array("Vacio"=>"white","Si"=>"green","No"=>"red","Sobrante"=>"yellow");
  foreach(array_keys($casos) as $caso){
    $report.="<tr><td></td><td>$caso</td>";
    $style="style='background:".$casos[$caso]."'";
    foreach($fields as $field){
      if($field=="recurso" or $field=="capacidad"){continue;}
      $report.="<td $style>".$count[$field][$caso]."</td>";
    }
    $report.="</tr>";
  }
  $table="<table border=1>$header$report$content</table>";
  echo $table;
}else if(isset($_GET["Resumen"])){
  shell_exec("python salomon-reporte.py coincidencias");
  $out=shell_exec("cat salomon-mismatches.txt");
  echo "Mismatches:";
  echo "<pre>$out</pre>";
}else{
//////////////////////////////////////////////////////////////
//LISTA
//////////////////////////////////////////////////////////////
echo<<<REPORTES
<ul>
<li><a href="?HorarioAulas">Horario por aula</a></li>
<li><a href="?HorarioActividades">Horario por actividad</a></li>
<li><a href="?Coincidencias">Coincidencias</a></li>
<li><a href="?Resumen">Resumen de Coincidencias</a></li>
</ul>
REPORTES;
}
?>
