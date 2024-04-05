## Extending Libraries/Packages
Here are a couple of examples of how I make my data science workflow a little more convenient as it relates to extracting, cleaning, and summarizing data with pandas and SQLalchemy, but especially pandas_flavor (yum). We never want to store intermediate data sets in production code if it can be avoided, which is the major motivation for chaining methods in a scalable data science workflow. While you can "monkey-patch" a library to 'add' a method you would like to chain, this is not the best practice and can backfire when sharing your ecosystem, attempting to avoid version control issues, or possibly overriding a pre-existing method yikes! Ultimately, the biggest motivation for extending a package compared to just writing the same method as a function in your script is that it allows you to reliably chain your custom methods. then just import your package with the method you like as one might expect:

#### For example: ```from <package>.<folder_containing_your_extended_methods> import <your_method>

### Pandas Flavoring and Decorators: See ```time_series.py``` for Use case
- Many data scientists manipulate data in Python through a classic combo of NumPy and Pandas (although Polars are getting pretty enticing...) 
- Pandas is built on the Data.Frame data structure. While we are making extensions to the Pandas library, it does not know these methods operate on a Data.Frame. I can't chain!!! Infinite sadness ensues
- ```pandas_flavor``` to the rescue!
  - We can use a [decorator](https://www.geeksforgeeks.org/decorators-in-python/) to modify the behavior of my ```summarize_by_time``` method (or any method; Decorators are wildly useful)
  - In using the ```pandas_flavor``` library, we can register the ```summarize_by_time``` as a method that takes a Data.Frame object with ```@pf.register_dataframe_method```
                Crisis averted, we can now ```df.summarize_by_time(...)``` where the ```data``` argument is already registered as ```df```. Chain away, dear readers
- An insightful article about how pandas_flavor can make your workflow a little smoother see this great [Medium Article by Luke Garzia](https://medium.com/@garzia.luke/wrangling-pandas-with-pandas-flavor-26007e90d53f)
- Similar in *flavor* (heh): the Pandas ```pipe()``` method with some solid examples in the [documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pipe.html)
  - Note: you'll still have to pandas flavor it up depending on what methods (ie ```summarize_by_time```) you are piping.  

### Happy Chaining!
