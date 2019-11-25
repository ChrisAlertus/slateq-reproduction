from user import User
from document import Document

class generalConditionalChoiceUser(User):
    
    def userChoice(self, recommendations):
        """
        Computes the relative likelihoods of choosing any of the (k+1) 
        options (including null item) presented in a slate of 
        recommendations based on the user's preference

        Args:
            recommendations(list document): a list of document objects 
                that were recommended to the user. Not including null
        Returns
            propensities (array float): probability distribution over 
                documents based on likelihood of being chosen
            choice (document) 
        """

        propensities = np.zeros(len(recommendations)+1)
        
        for idx, doc in enumerate(recommendations):
            # evaluate v(x_ij): user i , doc j
            propensities[idx] = self.inspectDocument(doc)
        
        # adding null document
        recommendations.append(None)
        propensities[-1] = self.nullInterest

        # changing doc interests to propensities
        propensities = propensities / propensities.sum()

        # sample from user choice model
        userChoice = np.random.choice(a=recommendations, p=propensities)

        if userChoice is None:
            userChoiceDocument = Document(name="null")
        else:
            userChoiceDocument = userChoice

        return propensities, userChoiceDocument