


<h1>About The App</h1>
<p>This Web app Classifies an uploaded image of a fruit and displays additional information about the identified fruit.</p>

<h2>NOTICE:</h2>
<p>The Following Instructions Are for Linux OS.</p>

<h2>How To Run the App:</h2>

<p>First the repository must be cloned by executing the following command on your terminal:</p>
   
   
    git clone https://github.com/MertAkkad/Fruit-classifier.git

     
<p>You can run the app <strong>AUTOMATICALLY</strong> by running the <code>run.sh</code> file (Double left-click or right-click + run as a program).</p>

<p><strong>NOTE:</strong> The virtual environment will be created and the required modules will be installed automatically.</p>

<p>You can also run the app <strong>MANUALLY</strong> by executing the following commands on your terminal:</p>

</pre>
- Navigate to project directory:</pre>
      
      cd Fruit-classifier
      
</pre>
- Create virtual environment:</pre>
      
      python3 -m venv myenv
 </pre>     
- Activate virtual environment:</pre>
      
      source venv/bin/activate
 </pre>   
- Install the required modules:</pre>
      
      pip install -r requirements.txt
</pre>    
- Run app.py:</pre>
      
      python3 app.py


<h2>How to Navigate to the Webpage:</h2>
<p>After running the app, the terminal will pop up where you can find the address <code>http://localhost:5000</code> and follow the link to open the app in your browser.</p>
<h2>Train/Customize your own model:</h2>
<p>If you check the train.py file you can see command lines Tagged with "(can be customized)" indicating that these parts of the code can be customized.This way you can generate classifiers for other subject(cars, vegetables etc.)</p>

</body>
</html>





