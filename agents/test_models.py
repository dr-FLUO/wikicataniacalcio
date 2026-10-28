from __future__ import annotations

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from datetime import date
from pathlib import Path

from pydantic import ValidationError

from models import (
    ExternalCorrectionSubmission,
    GoalEvent,
    JudicialStep,
    LegalDossierPayload,
    MatchReportPayload,
    SeasonPayload,
    SourceCitationPayload,
    UltrasGroupPayload,
    VaultComplianceLinter,
    WikiDeps,
)


def run_validation_suite() -> None:
    base_dir = Path(__file__).resolve().parent.parent
    deps = WikiDeps.load(base_dir)
    assert len(deps.known_slugs) >= 50, f"Attese >= 50 entità nel registro, trovate {len(deps.known_slugs)}"
    assert deps.resolve_slug("Ciccio Falange") == "tifoseria/biografie/ciccio-famoso"
    assert deps.resolve_slug("Stadio Cibali") == "stadio/angelo-massimino"
    print(f"[OK] Registro Entità caricato con successo: {len(deps.known_slugs)} entità canoniche e {len(deps.alias_to_slug)} alias risolti.")

    # 1. Test Stagione 2012-2013 valida (quadratura algebrica + fonti obbligatorie)
    s_2012_13 = SeasonPayload(
        title="Stagione 2012-2013 — Il Record Storico di 56 Punti in Serie A",
        description="Stagione 2012-2013 del Calcio Catania in Serie A: 8º posto e record storico di 56 punti con Rolando Maran.",
        slug="stagioni/2012-2013",
        season_label="2012-2013",
        club_entity_slug="societa/2004-era-pulvirenti",
        figc_matricola="11700",
        division="Serie A",
        division_tier=1,
        president_slugs=["societa/presidenti/antonino-pulvirenti"],
        coach_slugs=["tesserati/allenatori/rolando-maran"],
        matches_played=38,
        wins=15,
        draws=11,
        losses=12,
        goals_for=50,
        goals_against=46,
        points_per_win_regime=3,
        points_field=56,
        points_penalty=0,
        points_final=56,
        final_position=8,
        top_scorer_slug="tesserati/calciatori/gonzalo-bergessio",
        top_scorer_goals=13,
        sources=[
            SourceCitationPayload(
                author="Lega Nazionale Professionisti Serie A",
                title="Archivio Statistico Serie A TIM 2012-2013",
                publisher="Lega Serie A",
                year=2013,
                reference="Classifica ufficiale e tabellini 38ª giornata",
            )
        ],
    )
    assert s_2012_13.points_final == 56
    print("[OK] Validazione algebrica SeasonPayload (2012-2013: 15*3 + 11 = 56 pt) superata.")

    # 2. Test Errore Algebrico bloccato automaticamente da Pydantic v2
    try:
        SeasonPayload(
            title="Stagione Allucinata",
            description="Test di intercettazione errore matematico nei punti in classifica da parte di un LLM.",
            slug="stagioni/2015-2016",
            season_label="2015-2016",
            club_entity_slug="societa/2004-era-pulvirenti",
            figc_matricola="11700",
            division="Lega Pro",
            division_tier=3,
            president_slugs=["societa/presidenti/antonino-pulvirenti"],
            coach_slugs=["tesserati/allenatori/pasquale-marino"],
            matches_played=34,
            wins=12,
            draws=13,
            losses=9,
            goals_for=37,
            goals_against=34,
            points_per_win_regime=3,
            points_field=49,
            points_penalty=10,
            points_final=45,  # ERRATO: 49 - 10 deve fare 39, non 45!
            final_position=13,
            top_scorer_slug="tesserati/calciatori/francesco-lodi",
            top_scorer_goals=7,
            sources=[
                SourceCitationPayload(
                    author="FIGC", title="Comunicato Ufficiale TFN", publisher="FIGC", year=2015
                )
            ],
        )
        raise AssertionError("SeasonPayload avrebbe dovuto sollevare ValidationError per mancata quadratura penalizzazione!")
    except ValidationError:
        print("[OK] Guardrail Algebrico attivo: rigettata classifica con quadratura penalizzazione errata.")

    # 3. Test Obbligo Citazione Fonti (Art. 70 L. 633/1941)
    try:
        UltrasGroupPayload(
            title="Falange d'Assalto",
            description="Storia della Falange d'Assalto Rossazzurra fondata nel 1979 in Curva Sud.",
            slug="tifoseria/curva-sud/falange-d-assalto",
            foundation_year=1979,
            origin_district="Castello Ursino",
            stadium_sector="Curva Sud - Anello Inferiore",
            sources=[],  # ERRATO: array fonti vuoto!
        )
        raise AssertionError("UltrasGroupPayload avrebbe dovuto sollevare ValidationError per assenza di fonti!")
    except ValidationError:
        print("[OK] Guardrail Copyright UE attivo: rigettata pagina priva di fonti bibliografiche certificate.")

    # 4. Test Audit di tutti i file Markdown nel Vault content/
    vault_dir = base_dir / "content"
    md_files = sorted(vault_dir.rglob("*.md"))
    if md_files:
        failed = 0
        for md_file in md_files:
            res = VaultComplianceLinter.audit_file(md_file)
            if not res.is_valid:
                failed += 1
                print(f"[ERRORE LINTER] {res.file_path}: {res.errors}")
        if failed > 0:
            sys.exit(1)
        print(f"[OK] Audit VaultComplianceLinter superato al 100% su {len(md_files)} file Markdown in content/.")


if __name__ == "__main__":
    run_validation_suite()
