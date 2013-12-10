<html>

<head>
<title>Search</title>
</head>


    <body>
	
	<b><center><font size=7>Corruption-Themed Posts on Sina Weibo: <br>Visualisation and Analysis</font></center></b><p>
	
	    <center><form name="form" method="post">
        Enter Sina Weibo Search Terms: <input type="text" name="text_box" size="50"/>
        <input type="submit" name ="submit1" id="search-submit" value="Submit"/>
        <p>
		
		<center>Current Search Terms: <p>
		<?php echo file_get_contents("terms.txt");?><p>
		<input type="submit" name ="submit2" id="submit" value="Accept current search terms"/></form></center>		   
				   
		
    </body>
</html>


<?php

  // submit 1 pressed

if (isset($_POST['submit1'])) { //only do file operations when appropriate
        $a = $_POST['text_box'];
        $myFile = "terms.txt";
        $fh = fopen($myFile, 'w') or die("can't open file");
		fwrite($fh, $a);
        fclose($fh);
		//$command = 'python scripts/hello.py';
		$command = 'python scripts/SearchForStringInTweets.py';
		exec($command, $return);
		echo $return[0];
		header ("location: done.html");
    }

  // submit 2 pressed

else if (isset($_POST['submit2'])) {
		header ("location: visual.html");
}
?>

