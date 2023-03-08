This Project is an experiment to demonstrate a few alternative design choices for web development with flask and mysql

### Here are a few of the changes:
- Utilization of a base class for our models to reduce code duplication
- Using dataclasses for our models to simplify our constructors and implement some helpful dunder methods such as \_\_eq\_\_
- Using properties to handle our relationships (this is technically less efficient, but much more readable, and the efficiency difference is negligable at this scale)
- Custom decorators for our controller routes to reduce code duplication and increase readability
- utilizing url_for for redirects since it is more consistent, and also is more clear on how to pass variables with a redirect
- Using `app.get` and `app.post` instead of `app.route` and specifying the methods as it is more consistent with other stacks, and is more readable
- Decouple message flashing from the validate method and put it into the controllers instead, since it is an interaction with the templates. This also makes it so our models don't have to change whether we are doing ajax validations or regular validations, only the controller does
- using category filters for our error messages, so they can be displayed below each input instead of grouped together in one spot
