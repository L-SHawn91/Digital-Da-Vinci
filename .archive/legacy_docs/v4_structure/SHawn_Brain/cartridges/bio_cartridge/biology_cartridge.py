
import os
import json
import logging
from typing import List, Dict, Any, Optional, Tuple

# FAISS and sentence-transformers are heavy dependencies, so we prepare for them.
# In a real environment, these would be installed.
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KnowledgeBase:
    """
    Manages a knowledge base using FAISS for efficient similarity search.
    This class is prepared to handle vector embeddings of text data.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', dimension: int = 384):
        """
        Initializes the KnowledgeBase.

        Args:
            model_name (str): The name of the sentence-transformer model to use.
            dimension (int): The dimension of the vectors produced by the model.
        """
        if not FAISS_AVAILABLE:
            logging.warning("FAISS or sentence-transformers not found. KnowledgeBase will have limited functionality.")
            self.model = None
            self.index = None
            self.documents: List[str] = []
        else:
            self.model = SentenceTransformer(model_name)
            self.index = faiss.IndexFlatL2(dimension)
            self.documents: List[str] = []
            logging.info(f"KnowledgeBase initialized with model '{model_name}'.")

    def add_documents(self, docs: List[str]):
        """
        Adds documents to the knowledge base.

        Args:
            docs (List[str]): A list of documents (strings) to add.
        """
        if not self.model or not self.index:
            logging.error("Cannot add documents. KnowledgeBase is not properly initialized.")
            return

        self.documents.extend(docs)
        embeddings = self.model.encode(docs, convert_to_numpy=True)
        self.index.add(embeddings.astype('float32'))
        logging.info(f"Added {len(docs)} new documents. Total documents: {self.index.ntotal}.")

    def search(self, query: str, k: int = 5) -> List[Tuple[str, float]]:
        """
        Searches the knowledge base for similar documents.

        Args:
            query (str): The query string.
            k (int): The number of similar documents to return.

        Returns:
            List[Tuple[str, float]]: A list of tuples, each containing a document and its similarity score.
        """
        if not self.model or not self.index or self.index.ntotal == 0:
            logging.warning("Knowledge base is empty or not initialized. Cannot perform search.")
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True).astype('float32')
        distances, indices = self.index.search(query_embedding, k)

        results = []
        for i in range(len(indices[0])):
            doc_index = indices[0][i]
            if doc_index < len(self.documents):
                results.append((self.documents[doc_index], distances[0][i]))
        return results

    def save(self, index_path: str, docs_path: str):
        """Saves the FAISS index and documents."""
        if not FAISS_AVAILABLE:
            logging.error("Cannot save. FAISS not available.")
            return
        faiss.write_index(self.index, index_path)
        with open(docs_path, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f)
        logging.info(f"KnowledgeBase saved to {index_path} and {docs_path}.")

    def load(self, index_path: str, docs_path: str):
        """Loads the FAISS index and documents."""
        if not FAISS_AVAILABLE:
            logging.error("Cannot load. FAISS not available.")
            return
        if os.path.exists(index_path) and os.path.exists(docs_path):
            self.index = faiss.read_index(index_path)
            with open(docs_path, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
            logging.info(f"KnowledgeBase loaded from {index_path} and {docs_path}. Total documents: {self.index.ntotal}.")
        else:
            logging.error(f"Could not find files at {index_path} or {docs_path}.")


class BiologyCartridge:
    """
    A specialized cartridge for biological research, focusing on uterine organoids,
    experimental design, and literature analysis, based on Dr. SHawn's expertise.
    """

    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        """
        Initializes the BiologyCartridge.
        """
        self.name = "BiologyCartridge"
        self.version = "1.0.0"
        self.author = "Gemini 2.5 Pro for Dr. SHawn"
        self.knowledge_base = knowledge_base if knowledge_base else (KnowledgeBase() if FAISS_AVAILABLE else None)
        
        # Core knowledge related to uterine organoids
        self.uterine_organoid_protocols = {
            "endometrial_epithelial_organoids": {
                "source": "Human endometrial tissue or iPSCs",
                "key_markers": ["FOXA2", "PAX8", "KRT7", "KRT8"],
                "culture_medium": ["Matrigel", "Advanced DMEM/F12", "B27", "N2", "EGF", "Noggin", "R-spondin1", "Wnt3a"],
                "differentiation_factors": ["Estradiol (E2)", "Progesterone (P4)"],
                "applications": ["Modeling menstrual cycle", "Implantation studies", "Endometriosis research"]
            },
            "endometrial_stromal_organoids": {
                "source": "Human endometrial stromal cells",
                "key_markers": ["Vimentin", "CD13", "FOXO1"],
                "culture_medium": ["DMEM/F12", "FBS", "ITS", "Cholesterol"],
                "differentiation_factors": ["cAMP", "E2", "Medroxyprogesterone acetate (MPA) for decidualization"],
                "applications": ["Decidualization studies", "Stromal-epithelial interaction modeling"]
            }
        }
        logging.info(f"{self.name} v{self.version} initialized.")

    def get_organoid_protocol(self, organoid_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a protocol for a specific type of uterine organoid.

        Args:
            organoid_type (str): The type of organoid (e.g., "endometrial_epithelial_organoids").

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the protocol, or None if not found.
        """
        protocol = self.uterine_organoid_protocols.get(organoid_type)
        if not protocol:
            logging.warning(f"Protocol for '{organoid_type}' not found.")
        return protocol

    def design_experiment(self, objective: str, variables: List[str], controls: List[str]) -> Dict[str, Any]:
        """
        Designs a basic experimental plan based on an objective.

        Args:
            objective (str): The main goal of the experiment.
            variables (List[str]): The variables to be tested.
            controls (List[str]): The control groups for the experiment.

        Returns:
            Dict[str, Any]: A structured experimental plan.
        """
        if not objective or not variables:
            raise ValueError("Objective and variables are required for experimental design.")
            
        plan = {
            "title": f"Experimental Design: {objective}",
            "objective": objective,
            "hypothesis": "A generated hypothesis based on the objective and variables.",
            "experimental_groups": [],
            "control_groups": controls,
            "readouts": ["qPCR for gene expression", "Immunofluorescence for protein localization", "Morphological analysis"],
            "timeline_weeks": 4,
            "knowledge_search_query": f"experimental design for {objective} with variables {', '.join(variables)}"
        }

        for i, var in enumerate(variables):
            plan["experimental_groups"].append({
                "group_id": f"Exp_{i+1}",
                "condition": var,
                "description": f"Group testing the effect of {var}."
            })

        if self.knowledge_base:
            related_docs = self.knowledge_base.search(plan["knowledge_search_query"])
            plan["related_literature"] = [doc for doc, score in related_docs]
        
        logging.info(f"Generated experimental design for: {objective}")
        return plan

    def analyze_paper_abstract(self, abstract: str) -> Dict[str, Any]:
        """
        Performs a simple analysis of a scientific paper's abstract.

        Args:
            abstract (str): The abstract text of the paper.

        Returns:
            Dict[str, Any]: A dictionary with extracted key information.
        """
        if not isinstance(abstract, str) or len(abstract) < 50:
            raise ValueError("A substantial abstract string is required for analysis.")

        # Simple keyword-based extraction
        keywords = ["organoid", "endometrium", "stem cell", "differentiation", "tissue engineering", "implantation", "decidualization"]
        found_keywords = [kw for kw in keywords if kw in abstract.lower()]

        sentences = abstract.split('. ')
        
        analysis = {
            "summary": " ".join(sentences[:2]),  # A simple summary (first two sentences)
            "keywords": found_keywords,
            "potential_methods": [s for s in sentences if "method" in s.lower() or "protocol" in s.lower()],
            "potential_results": [s for s in sentences if "result" in s.lower() or "showed" in s.lower() or "demonstrated" in s.lower()],
            "relevance_score": len(found_keywords) / len(keywords)
        }
        
        logging.info(f"Analyzed abstract, found {len(found_keywords)} relevant keywords.")
        return analysis

# --- Test Functions ---

def run_tests():
    """
    Runs a suite of tests for the BiologyCartridge and its components.
    """
    print("--- Running BiologyCartridge Tests ---")

    # 1. Test Cartridge Initialization
    print("\n[1] Testing Cartridge Initialization...")
    try:
        cartridge = BiologyCartridge()
        assert cartridge.name == "BiologyCartridge"
        assert "1.0.0" in cartridge.version
        print("SUCCESS: Cartridge initialized correctly.")
    except Exception as e:
        print(f"FAILED: Cartridge initialization error: {e}")

    # 2. Test Organoid Protocol Retrieval
    print("\n[2] Testing Organoid Protocol Retrieval...")
    protocol = cartridge.get_organoid_protocol("endometrial_epithelial_organoids")
    assert protocol is not None
    assert "Matrigel" in protocol["culture_medium"]
    print("SUCCESS: Retrieved epithelial organoid protocol.")
    
    protocol_fail = cartridge.get_organoid_protocol("non_existent_organoid")
    assert protocol_fail is None
    print("SUCCESS: Handled non-existent protocol correctly.")

    # 3. Test Experimental Design
    print("\n[3] Testing Experimental Design...")
    try:
        objective = "Test the effect of novel growth factor 'GF-X' on endometrial organoid growth"
        variables = ["GF-X (10 ng/mL)", "GF-X (50 ng/mL)"]
        controls = ["No GF-X (vehicle control)"]
        plan = cartridge.design_experiment(objective, variables, controls)
        assert plan["objective"] == objective
        assert len(plan["experimental_groups"]) == 2
        assert "Exp_1" in plan["experimental_groups"][0]["group_id"]
        print("SUCCESS: Experimental design created successfully.")
    except ValueError as e:
        print(f"FAILED: Experimental design validation error: {e}")
    except Exception as e:
        print(f"FAILED: An unexpected error occurred during experimental design: {e}")

    # 4. Test Paper Abstract Analysis
    print("\n[4] Testing Paper Abstract Analysis...")
    try:
        sample_abstract = (
            "Here we describe a novel method for generating human endometrial organoids from induced pluripotent stem cells (iPSCs). "
            "Our protocol significantly improves differentiation efficiency. "
            "The resulting organoids exhibit key markers of endometrial epithelium and respond to hormonal stimuli. "
            "These results showed that our model is suitable for studying uterine biology and diseases like endometriosis."
        )
        analysis = cartridge.analyze_paper_abstract(sample_abstract)
        assert "organoid" in analysis["keywords"]
        assert "stem cell" in analysis["keywords"]
        assert analysis["relevance_score"] > 0
        assert len(analysis["potential_methods"]) > 0
        print("SUCCESS: Paper abstract analyzed correctly.")
    except ValueError as e:
        print(f"FAILED: Abstract analysis validation error: {e}")
    except Exception as e:
        print(f"FAILED: An unexpected error occurred during abstract analysis: {e}")
        
    # 5. Test KnowledgeBase (if available)
    print("\n[5] Testing Knowledge Base...")
    if not FAISS_AVAILABLE:
        print("SKIPPED: FAISS or sentence-transformers not installed.")
    else:
        try:
            kb = KnowledgeBase()
            cartridge_with_kb = BiologyCartridge(knowledge_base=kb)
            docs = [
                "Uterine organoids are 3D structures that mimic the endometrium.",
                "Tissue engineering combines cells, materials, and suitable biochemical factors.",
                "Stem cell differentiation is the process where a cell changes to a more specialized type."
            ]
            kb.add_documents(docs)
            assert kb.index.ntotal == 3
            print("SUCCESS: Documents added to KnowledgeBase.")

            search_results = kb.search("endometrial models")
            assert len(search_results) > 0
            assert "organoids" in search_results[0][0]
            print(f"SUCCESS: Search returned relevant result: '{search_results[0][0]}'")

            # Test saving and loading
            index_path = "test_kb.index"
            docs_path = "test_kb_docs.json"
            kb.save(index_path, docs_path)
            assert os.path.exists(index_path)
            
            kb_new = KnowledgeBase()
            kb_new.load(index_path, docs_path)
            assert kb_new.index.ntotal == 3
            print("SUCCESS: KnowledgeBase saved and loaded successfully.")
            
            # Cleanup
            os.remove(index_path)
            os.remove(docs_path)

        except Exception as e:
            print(f"FAILED: KnowledgeBase test error: {e}")
            
    print("\n--- All Tests Completed ---")


if __name__ == '__main__':
    # This block allows the script to be run directly to perform tests.
    run_tests()
    
    # Example usage of the cartridge
    # cartridge = BiologyCartridge()
    # protocol = cartridge.get_organoid_protocol("endometrial_epithelial_organoids")
    # print("\n--- Example Usage ---")
    # print("Protocol for Epithelial Organoids:", json.dumps(protocol, indent=2))
    
    # design = cartridge.design_experiment("Test new factor", ["Factor A"], ["Control"])
    # print("\nExperimental Design:", json.dumps(design, indent=2))

