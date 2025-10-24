Hello! This is the core node of the planning of Recept to inköpslista. 

Some thoughts:
Recipes stored in JSON.
	Extensible, integrates well to Python and easy to read by human

Host the app on a GitHub repo

Use Streamlit for backend to frontend connection.

Structure of app:
	Option to scan new recipes - also to check if everything went well for manual tinkering.
	Shopping list creator, based on what we add to this week's dinners.
		First thing ought to be just adding all ingredients to a list. This WORKS, but is not that streamlined.
			A problem initially spotted would be that units are not always the same (tbsp + tsp), perhaps when streamlining we can sum it up for ingredients with common name.
				Ingridents with common name needs to have a synonym list from different recipes if we want to have it on a large scale. 
	Wish for the shopping list to be interactable (you can tick off what you have at home or add it to ICA shopping list)