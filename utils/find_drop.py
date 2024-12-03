from abc import ABC, abstractmethod

class CompareDrop(ABC) : 
    @abstractmethod
    def significant_drop(self) : 
        raise NotImplementedError("`significant_drop` method not implemented")
    
    @abstractmethod
    def historical_change(self) : 
        raise NotImplementedError("`historical_change` method not implemented")
    
    @abstractmethod 
    def drop_recovery(self) : 
        raise NotImplementedError("`drop_recovery` method not implemented")
    
    @abstractmethod 
    def drop_continuation(self) : 
        raise NotImplementedError("`drop_continuation` method not implemented")


