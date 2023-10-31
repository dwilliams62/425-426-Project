<!DOCTYPE html> 
<html> 
      
<head> 
    <title> 
        How to call PHP function 
        on the click of a Button ? 
    </title> 
</head> 
  
<body style="text-align:center;"> 
    <h1 style="color:green;"> 
        GeeksforGeeks 
    </h1> 
      
    <h4> 
        How to call PHP function 
        on the click of a Button ? 
    </h4> 
      
    <form method="post"> 
        <input type="submit" name="button1"
                value="Button1"/> 
          
        <input type="submit" name="button2"
                value="Button2"/> 
    </form> 

    <?php
        if(isset($_POST['button2'])) { 
            echo "This is Button2 that is selected"; 
        }
        echo "an attempt";
        require_once __DIR__ . '/vendor/autoload.php';
        use Exception;
        use MongoDB\Client;
        use MongoDB\Driver\ServerApi;
        echo " got past the use";
        echo extension_loaded("mongodb") ? "loaded\n" : "not loaded\n";
        //Replace the placeholder with your Atlas connection string
        $uri = 'mongodb+srv://dwilliams62:biomez!!!@cluster0.u9t9rco.mongodb.net/';
        echo " got past setting uri";
        //Create a new client and connect to the server
        $client = new MongoDB\Driver\Manager($uri);
        echo "end setup";

        if(isset($_POST['button1'])) { 
            echo "button 1 pressed";
            try {
                //Send a ping to confirm a successful connection
                $client->selectDatabase('admin')->command(['ping' => 1]);
                echo "Pinged your deployment. You successfully connected to MongoDB!\n";
            } catch (Exception $e) {
                echo "failure";
                printf($e->getMessage());
            } 
        } 
        if(isset($_POST['button2'])) { 
            echo "This is Button2 that is selected"; 
        } 
    ?> 

</body> 
  
</html> 