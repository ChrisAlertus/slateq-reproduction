from abc import ABC, abstractmethod
import numpy as np
from document import Document
from probability_distributions import get_truncated_normal

# v(s,i) where i is the null item, constant for all users
NULL_INTEREST = -0.3
# specified in paper: % movmenet beween interest level and extreme for interest
y = 0.3 
# specified in paper 
DEFAULT_BUDGET = 200

class User(ABC):

    def __init__(self, T, fanatic_ratio=1):
        """
        Constructor for user class: 
            Constructs a new user including their original interests
        
        Args:
            
            T (int) : number of topics that the user could be interested in

            fanatic_ratio (float): a weighting factor that denotes how much the user's 
                satisfaction with a document weighs the quality of the document
                d against their interest in the document. 1 => only care about 
                quality 
            
        Returns
            User (object)
        """
        
        # pInterest: ~U(-1,1)
        self.interests =  np.random.uniform(-1,1,size=T)
        self.fanatic_ratio = fanatic_ratio
        self.nullInterest = NULL_INTEREST
        # static attribute
        self.gender = "male" if np.random.binomial(n=1,p=0.5) == 0 else "female"
        # logging user behaviour history as features
        self.historicalTopicViews = np.zeros(T)
        self.historicalCumTopicTime = np.zeros(T)
        self.historicalCumTopicQuality = np.zeros(T)
        self.historicalNumSessions = 0
        self.historicalTimeSpent = 0
        self.historicalCumBudget = 0
        self.historicalCumChoicesPerSession = 0.0
        self.historicalMaxChoicesPerSession = 0
        self.historicalMinChoicesPerSession = 0
        self.historicalNumNullChoice = 0
        self.historicalCumNullChoicePerSession = 0.0
        # current session attributes
        self.numSessionChoices = 0
        self.lastChoice = Document(name="null")
        self.currBudget = 0
        # last session attributes
    
    # user interaction methods
    def inspectDocument(self, document):
        """
        Inspects document and computes an interest value : I(u,d) based on user
        interest compatibility with the document's topic(s)

        Args:
            document(object): object containing the document the user is 
                examining to determine their level of interest

        Returns 
            interestValue (float): scalar measure of the user's interest in document
        """
        
        interestValue = np.dot(self.interests , document.topic)
        return  interestValue

    def computeDocumentSatisfaction(self, document):
        """
        Inspects document and computes satisfaction : S(u,d) based on user
        interest in the document, and the quality of the document

        Args:
            document(object): object containing the document the user is 
                interacting with

        Returns 
            satisfactionValue (float): scalar measure of the user's interest 
            in document
        """

        
        qualityValue = self.fanatic_ratio * document.quality
        interestValue = (1- self.fanatic_ratio) * self.inspectDocument(document)
        # satisfaction is convex sum of interest and doc quality
        satisfactionValue = qualityValue + interestValue
        
        return satisfactionValue

    def updateStats(self, document, portionConsumed):
        """
        Updates stats on user history based on them consuming a specific 
            document

        Args:
            document(object): object containing the document the user is 
                interacting with
            portionConsumed (float): percentage of full doc length that 
                the user interacted with the item. Assumed 1

        Returns 
            None (updates the historical attributes)
        """

        self.historicalNumSessions += 1
        # static counts
        self.historicalTopicViews += document.topic
        self.historicalTimeSpent += min(document.length * portionConsumed,\
                                        self.currBudget)
        # cumulative counts
        self.historicalCumTopicTime += min(self.currBudget, \
            (document.topic * portionConsumed * document.length))
        self.historicalCumTopicQuality += document.topic * document.quality
        if document.name == "null":
            self.historicalNumNullChoice += 1
        # current session attributes
        self.numSessionChoices += 1
        self.lastChoice = document

    def consumeDocument(self, recommendations):
        """
        User makes a choice of document from the slate of recommendations 
            presented. Computes stats on user history as well as user interest
            dynamics 

        Args:
            recommendations(list Document): list of document objects corresponding 
                to the slate the user is interacting with

        Returns 
            None (updates the user object)
            Chooses a document from slate according to user choice model
            Updates stats on user based on doc choice
            Updates user interests based on 
            Updates remaining buget within session
        """
        #TODO
        # Assume portion decided when sampling from dynamics specifications 
        
        portionConsumed = 1 
        chosenDoc = self.userChoice(recommendations=recommendations)
        
        # update stats on doc choice
        
        self.updateStats(document=chosenDoc, portionConsumed=portionConsumed)
        
        # update user interest profile
        
        satisfactionValue = self.computeDocumentSatisfaction(document=chosenDoc)
        
        # proportion of movement from position relative to extreme
        # y = np.random.uniform(low=0, high=1)
        # formula for change in topic interst
        deltaIt = (-y * abs(self.interests) + y) * - self.interests
        
        # so only the interest in chosendoc topic gets updated 
        deltaIt *= chosenDoc.topic 
        
        # sampling to get pos/negative interest 
        pInterestDirection = (self.inspectDocument(chosenDoc) + 1 )/2
        
        if np.random.binomial(n=1,p=pInterestDirection) == 1:
            self.interests += deltaIt
        else:
            self.interests -= deltaIt
        
        # update budget
        
        satisfcationBonus = (0.9/3.4)* chosenDoc.length * satisfactionValue
        self.currBudget -= chosenDoc.length + satisfcationBonus

    def userSession(self, corpus, budget, m, k):
        """
        Let the current user experience a session of being recommended items and
        logging interactions. Ends when session time budget hits 0.

        Args:
            corpus (dict of Document) : catalogue of content that could be 
                recommended to user
            budget(int): amount of time available to watch videos on a day

            m (int) : the number of candidate documents returned by a shorlist
                upstream process that the slateQ would later re-rank
            k (int) : the number of items in a slate
        Returns:
            None: simulates a user's session repeatedly consuming docs
                until budget runs out and logging interactions to a pandas df
        """
        # TODO
        # Set the portion of document consumed when drawing doc
        # as integer, make 
        # get_truncated_normal(mean=1,sd=0.6,low=0,upp=1) and round

        # update at start of session
        budget = DEFAULT_BUDGET
        # self.historicalCumBudget += budget
        # self.currBudget = budget


        # check if session over , since budget == 0

        # update at end of session:
        # self.historicalCumChoicesPerSession = 0.0
        # self.historicalMaxChoicesPerSession = 0.0
        # self.historicalMinChoicesPerSession = 0.0
        # self.historicalCumNullChoicePerSession = 0.0
        

        pass

    @abstractmethod
    def userChoice(self, recommendations):
        """
        Computes the relative likelihoods of choosing any of the (k+1) 
        options (including null item) presented in a slate of 
        recommendations based on the user's preference

        Args:
            recommendations(list document): a list of document objects 
                that 
        """
        raise NotImplementedError
# 
if __name__ == "__main__":
    pass