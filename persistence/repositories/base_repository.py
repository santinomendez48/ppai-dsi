from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Interfaz base para todos los repositorios"""
    
    @abstractmethod
    def save(self, entity: T) -> T:
        """Guarda una entidad en la base de datos"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        """Busca una entidad por su ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Obtiene todas las entidades"""
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """Elimina una entidad por su ID"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza una entidad existente"""
        pass

