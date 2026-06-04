import pytest
from backend.ai.scoring_engine import ScoringEngine
from backend.models import JobOffer, Profile, AnalysisResult


@pytest.fixture
def engine():
    return ScoringEngine(threshold=7.0)


@pytest.fixture
def profile():
    return Profile(
        tecnologias="Python, FastAPI, PostgreSQL, Docker, AWS",
        experiencia_anos=5,
        nivel_ingles="Avanzado",
        seniority="Senior",
    )


@pytest.fixture
def offer():
    return JobOffer(
        empresa="MixRank",
        cargo="Senior Python Developer",
        ubicacion="Remoto",
        link="https://example.com/job/1",
        descripcion="Python, AWS, Docker, PostgreSQL, Kubernetes",
        fuente="linkedin",
    )


@pytest.fixture
def analysis():
    return AnalysisResult(
        score=9.0,
        fortalezas=["Python", "Docker", "AWS"],
        debilidades=["Kubernetes"],
        recomendacion="Buena opción, podria aprender K8s",
    )


class TestScoringEngine:
    def test_score_calculation(self, engine, offer, profile, analysis):
        scored = engine.score(offer, profile, analysis)
        assert 0 <= scored.score_final <= 10
        assert scored.score_final > 0

    def test_classify_excelente(self, engine):
        scored = engine.score(
            JobOffer(empresa="A", cargo="B", ubicacion="Remoto", link="x", descripcion="Python Docker AWS PostgreSQL"),
            Profile(tecnologias="Python, Docker, AWS, PostgreSQL", experiencia_anos=5, nivel_ingles="Avanzado", seniority="Senior"),
            AnalysisResult(score=9.5, fortalezas=[], debilidades=[], recomendacion=""),
        )
        assert scored.clasificacion == "Excelente"

    def test_classify_descartada(self, engine):
        scored = engine.score(
            JobOffer(empresa="A", cargo="B", ubicacion="Presencial", link="x", descripcion="Java Spring C++"),
            Profile(tecnologias="Python, Django", experiencia_anos=1, nivel_ingles="Basico", seniority="Junior"),
            AnalysisResult(score=2.0, fortalezas=[], debilidades=[], recomendacion=""),
        )
        assert scored.clasificacion == "Descartada"

    def test_filter_best(self, engine, offer, profile, analysis):
        scored = engine.score(offer, profile, analysis)
        filtered = engine.filter_best([scored])
        if scored.score_final >= engine.threshold:
            assert len(filtered) == 1
        else:
            assert len(filtered) == 0

    def test_top_n(self, engine, offer, profile, analysis):
        scored_list = [engine.score(offer, profile, analysis) for _ in range(3)]
        top = engine.top_n(scored_list, n=2)
        assert len(top) <= 2
        assert all(s.score_final >= top[-1].score_final for s in top)
