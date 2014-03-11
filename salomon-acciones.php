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
echo "<h2><a href=?>Acciones</a></h2>";
echo "<h3>Ver tambien: <a href=salomon.php>Lista de Tablas</a>, <a href=salomon-reportes.php>Reportes</a></h2>";

//////////////////////////////////////////////////////////////
//REPORTES
//////////////////////////////////////////////////////////////
echo "Soluciones:".$_GET["Soluciones"];
if(false){
}else if(isset($_GET["Soluciones"])){
  if(false){
  }else if(!isset($_GET["haga"])){
echo<<<SOLUCIONES
<form>
  <input type='hidden' name='Soluciones' value='1'>
  Numero de soluciones: <input type='text' name='numero' value='10'><br/>
  semilla: <input type='text' name='seed' value='0'> (0 para aleatoriedad)
  <input type='submit' name='haga' value='Haga'>
</form>
SOLUCIONES;
  }else{
    $numero=$_GET['numero'];
    $semilla=$_GET['seed'];
    //$out=shell_exec("python salomon-solucion.py $numero $semilla &> $ROOTDIR/soluciones/salomon-soluciones.log");
    $out=shell_exec("python salomon-solucion.py $numero $semilla");
    shell_exec("echo '$out' > soluciones/salomon-soluciones.log");
    $out=shell_exec("cat soluciones/salomon-soluciones.log");
    echo "<pre>$out</pre>";
    echo "<a href=?Soluciones>Corre otras soluciones</a>";
  }     	    
}else if(isset($_GET["Cargar"])){
      if(false){
      }else if(!isset($_GET["carga"])){
	$lines=file("soluciones/salomon-soluciones.txt",FILE_IGNORE_NEW_LINES);
	$solstr="<ul>";
	$solstr.="<li><a href='?Cargar&carga=-1'>Reset completo</a></li>";
	$solstr.="<li><a href='?Cargar&carga=00000'>No solucion</a></li>";
	foreach($lines as $solution){
	  $parts=split(" ",$solution);
	  $solstr.="<li><a href='?Cargar&carga=$parts[0]'>Solucion $parts[0]</a>: $parts[1]</li>";
	}
	$solstr.="</ul>";
	$out=shell_exec("cat soluciones/salomon-soluciones.log");
echo<<<SOLUCIONES
Soluciones disponibles:
$solstr
<p>Reporte detallado</p>
<pre>
$out
</pre>
</form>
SOLUCIONES;
      }else{
	$solution=$_GET['carga'];
	if($solution>=0){
	  $out=shell_exec("python salomon-carga.py soluciones/salomon-$solution.sal");
	}else{
	  $out=shell_exec("python salomon-populate.py 2> /tmp/a");
	}
	echo "<pre>$out</pre>";
	echo "<a href=?Cargar>Carga otra solucion</a>";
      }     	    
}else{
//////////////////////////////////////////////////////////////
//LISTA
//////////////////////////////////////////////////////////////
echo<<<ACCIONES
<ul>
<li><a href="?Soluciones">Soluciones</a></li>
<li><a href="?Cargar">Cargar Soluciones</a></li>
</ul>
ACCIONES;
}
?>
