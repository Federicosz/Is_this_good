# Is this good: An exploration of American Branded food

This project aims to empower consumers to avoid "toxic" foods and help them select the best products to meet their goals. The project is based on the dataset provided by the USDA (U.S. Department of Agriculture) for the branded food release in October 2023. It intends to provide an easier and more efficient way for users to search for branded foods with specific nutrient and ingredient characteristics.

# libraries
- python 3.11
- Streamlit
- pymysql
- SQLAlchemy
- python-dotenv
- seaborn
- plotly

# key aspect

1. The nutrients selected for the app were: Protein, Fat, Carbohydrate, Calories, Fiber, Sodium, Suggar added, Cholesterol, Trans fat and Total sugars.
2. The clean dataset has more than 300k different products. Small changes such as flavor or size that didn't affect the nutrient composition were taken as duplicates.
3. The total size of the dataset is 3.1Gb.

# Demo

### Home
![home](https://github.com/Federicosz/Is_this_good/blob/main/pictures/homescreen_isthisgood.png) 

### Inicial Selection
![select food category(ies),food brand(s) and ingredient(s) to avoid](https://github.com/Federicosz/Is_this_good/blob/main/pictures/selection.png)

You can begin by choosing either the category or the brand. Once you make a selection, the app will automatically apply a filter based on your choice. To prevent any errors, please wait until this process is complete before making any other selections.

### Nutrient selection

![select and filter nutrients](https://github.com/Federicosz/Is_this_good/blob/main/pictures/nutrient_selection.png)

### Select food to compare

![branded food to compare](https://github.com/Federicosz/Is_this_good/blob/main/pictures/select_comparation_isthisgood.png)

To compare different food options in the graph, click on the "select" column of the "Product Available" table to add the desired food.

### Select a specific product

![specific product](https://github.com/Federicosz/Is_this_good/blob/main/pictures/spec_product_selection.png)

If you want more information on a specific product, you can select it from the list. This will show you details such as the nutrients, ingredients, and the relative amounts of fat, fiber, protein, and total sugar.

# Conclusion

1. **Limited Scope:** The current app approach relies on predefined food categories and may miss important food products. This could be addressed by expanding the dataset or refining the categorization process.
2. **Lack of Domain Understanding:** Without a deep understanding of the food industry, biases may influence decisions on what to include or exclude from the analysis. Seeking expert advice or conducting thorough research can help mitigate this issue.
3. **Data Cleaning Challenges:** too many food products with small variation or some process work in the sample but not in the all dataset.

# Future work

1. **Inclusion of Toxic Ingredients:** Adding data on toxic ingredients can enhance the analysis by providing insights into potential health risks associated with certain products. This could involve sourcing data from reputable sources or conducting toxicity assessments.
2. **Product Availability Information:** Incorporating data on where to find products can be valuable for consumers seeking specific items. This could involve mapping product availability across different retailers or locations.
3. **Implementation of a Suggestion Model:** Developing a suggestion model can improve the user experience by recommending suitable food products based on individual preferences, dietary requirements, or health goals. This could utilize machine learning algorithms and user feedback to refine recommendations over time.

## Acknowledgements

 - [Our Awesome Teacher](https://github.com/Rairocha)

## Authors

- [Federico Sarmiento Z.](https://github.com/Federicosz) [![Linkedin Badge](https://img.shields.io/badge/-federico_Sarmiento_Z-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://https://www.linkedin.com/in/fsarmientoz/)](https://www.linkedin.com/in/fsarmientoz/)
  

