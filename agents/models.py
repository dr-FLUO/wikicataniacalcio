from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator

# =====================================================================
# 1. REGISTRO DELLE ENTITÀ E DIPENDENZE (ENTITY REGISTRY)
# =====================================================================

@dataclass
class WikiDeps:
    """Dipendenze condivise per gli agenti di Squadra 1, Squadra 2 e FactCheckAgent."""
    registry_path: Path
    schema_path: Path
    vault_root: Path
    known_slugs: set[str]
    alias_to_slug: dict[str, str]

    @classmethod
    def load(cls, base_dir: Path) -> "WikiDeps":
        reg_file = base_dir / "data" / "entity_registry.json"
        registry_data = json.loads(reg_file.read_text(encoding="utf-8"))
        known_slugs = set(registry_data["entities"].keys())
        alias_map: dict[str, str] = {}
        for slug, meta in registry_data["entities"].items():
            alias_map[meta["canonical_name"].lower()] = slug
            for alias in meta.get("aliases", []):
                alias_map[alias.lower()] = slug
        return cls(
            registry_path=reg_file,
            schema_path=base_dir / "SCHEMA.md",
            vault_root=base_dir / "content",
            known_slugs=known_slugs,
            alias_to_slug=alias_map,
        )

    def resolve_slug(self, mention: str) -> Optional[str]:
        return self.alias_to_slug.get(mention.strip().lower())


# =====================================================================
# 2. MODELLI NORMATIVI UE: FONTI, DIRITTO D'AUTORE E ACCESSIBILITÀ
# =====================================================================

class SourceCitationPayload(BaseModel):
    """Fonte bibliografica, archivistica o giurisprudenziale obbligatoria (Art. 70 L. 633/1941)."""
    author: str = Field(min_length=2, description="Autore, curatore o ente (es. 'Buemi, Fontanelli, Quartarone, Russo, Solarino')")
    title: str = Field(min_length=3, description="Titolo dell'opera, sentenza o articolo")
    publisher: str = Field(min_length=2, description="Editore, tribunale o testata (es. 'GEO Edizioni', 'TAR Sicilia - Sez. Catania')")
    year: int = Field(ge=1900, le=2030, description="Anno di pubblicazione o pronuncia")
    reference: Optional[str] = Field(default=None, description="Pagine, numero sentenza o URL (es. 'pp. 184-191' o 'Ord. n. 1054/2003')")
    url: Optional[str] = Field(default=None, description="URL diretto HTTP/HTTPS alla fonte originale se risorsa web (es. 'https://www.mimmorapisarda.it/')")


ImageLicenseType = Literal[
    "Pubblico Dominio Italia (Art. 92 L. 633/1941 - >20 anni)",
    "Pubblico Dominio (Scadenza termini d'autore)",
    "Creative Commons CC BY-SA 4.0",
    "Creative Commons CC BY 4.0",
    "Marchio Storico ad uso descrittivo enciclopedico (Art. 21 CPI)",
    "Cortesia Archivio Storico Autorizzato",
]

class ImageCreditPayload(BaseModel):
    """Metadati obbligatori di copyright (Artt. 87-92 L. 633/1941) e accessibilità (WCAG 2.1 AA)."""
    image_path: str = Field(min_length=3, description="Percorso relativo dell'immagine nel vault")
    alt_text: str = Field(
        min_length=15,
        description="Testo alternativo descrittivo obbligatorio per screen reader (European Accessibility Act / WCAG 2.1 AA)"
    )
    author_or_archive: str = Field(min_length=2, description="Fotografo o archivio di provenienza (es. 'Archivio Mimmo Rapisarda')")
    year: Optional[int] = Field(default=None, ge=1900, le=2030)
    license_type: ImageLicenseType


# =====================================================================
# 3. MODELLI DI DOMINIO (CONTRATTO TRA SQUADRA 1 E SQUADRA 2)
# =====================================================================

# --- 3A. Stagione Agonistica ---

class SeasonPayload(BaseModel):
    """Contratto dati validato per una singola stagione agonistica (1929-Oggi)."""
    title: str
    description: str = Field(min_length=50, max_length=220, description="Meta description SEO/GEO")
    slug: str = Field(pattern=r"^stagioni/\d{4}-\d{4}$")
    season_label: str = Field(pattern=r"^\d{4}-\d{4}$")
    club_entity_slug: str = Field(pattern=r"^societa/[a-z0-9-]+$")
    figc_matricola: Literal["N/A (Pre-1946)", "11700", "955013"]
    division: str
    division_tier: int = Field(ge=1, le=6)
    president_slugs: list[str] = Field(min_length=1)
    coach_slugs: list[str] = Field(min_length=1)
    matches_played: int = Field(ge=0, le=50)
    wins: int = Field(ge=0)
    draws: int = Field(ge=0)
    losses: int = Field(ge=0)
    goals_for: int = Field(ge=0)
    goals_against: int = Field(ge=0)
    points_per_win_regime: Literal[2, 3]
    points_field: int
    points_penalty: int = Field(default=0, ge=0)
    points_final: int
    final_position: int = Field(ge=1, le=25)
    office_demotion: bool = Field(default=False)
    legal_dossier_slug: Optional[str] = Field(default=None, pattern=r"^vicende-legali/[a-z0-9-]+$")
    top_scorer_slug: str = Field(pattern=r"^tesserati/calciatori/[a-z0-9-]+$")
    top_scorer_goals: int = Field(ge=0)
    sources: list[SourceCitationPayload] = Field(
        min_length=1,
        description="Almeno una fonte bibliografica/ufficiale obbligatoria per conformità copyright"
    )
    image_credits: list[ImageCreditPayload] = Field(default_factory=list)

    @model_validator(mode="after")
    def verify_algebraic_standings(self) -> "SeasonPayload":
        if self.wins + self.draws + self.losses != self.matches_played:
            raise ValueError(
                f"Errore di quadratura gare ({self.season_label}): "
                f"V({self.wins}) + N({self.draws}) + P({self.losses}) != G({self.matches_played})"
            )
        expected_field_pts = (self.wins * self.points_per_win_regime) + self.draws
        if self.points_field != expected_field_pts:
            raise ValueError(
                f"Errore calcolo punti sul campo ({self.season_label}): "
                f"attesi {expected_field_pts} (regime {self.points_per_win_regime} pt/vittoria), "
                f"trovati {self.points_field}."
            )
        if self.points_field - self.points_penalty != self.points_final:
            raise ValueError(
                f"Errore quadratura penalizzazione ({self.season_label}): "
                f"{self.points_field} (campo) - {self.points_penalty} (pen.) != {self.points_final} (finali)."
            )
        return self


# --- 3B. Dossier Giudiziario ---

class JudicialStep(BaseModel):
    step_date: date
    body: str
    legal_norms: list[str] = Field(default_factory=list)
    decision_summary: str
    standings_impact: str


class SanctionedIndividual(BaseModel):
    full_name: str
    person_slug: Optional[str] = None
    role: str
    sanction_type: Literal["Inibizione", "Squalifica", "Ammenda", "Preclusione (Radiazione)"]
    ban_duration: str
    fine_euros: Optional[int] = Field(default=None, ge=0)
    preclusion: bool = Field(default=False)


class LegalDossierPayload(BaseModel):
    """Contratto dati validato per un nodo giudiziario autonomo."""
    title: str
    description: str = Field(min_length=50, max_length=220)
    slug: str = Field(pattern=r"^vicende-legali/[a-z0-9-]+$")
    date_start: date
    date_end: date
    season_slug: str = Field(pattern=r"^stagioni/\d{4}-\d{4}$")
    club_entity_slug: str = Field(pattern=r"^societa/[a-z0-9-]+$")
    figc_matricola: Literal["11700", "955013"]
    historical_context: str
    procedural_steps: list[JudicialStep] = Field(min_length=2)
    sanctions: list[SanctionedIndividual] = Field(default_factory=list)
    systemic_consequences: str
    related_entity_slugs: list[str]
    sources: list[SourceCitationPayload] = Field(min_length=1)
    image_credits: list[ImageCreditPayload] = Field(default_factory=list)

    @model_validator(mode="after")
    def verify_chronological_order(self) -> "LegalDossierPayload":
        dates = [step.step_date for step in self.procedural_steps]
        if dates != sorted(dates):
            raise ValueError("I gradi di giudizio in procedural_steps devono essere in ordine cronologico crescente.")
        if self.date_start > self.date_end:
            raise ValueError("date_start non può essere successiva a date_end.")
        return self


# --- 3C. Tabellino Gara Storica ---

class GoalEvent(BaseModel):
    minute: int = Field(ge=1, le=130)
    player: str
    team: Literal["Catania", "Avversario"]
    penalty: bool = False
    own_goal: bool = False


class MatchReportPayload(BaseModel):
    """Contratto dati validato per un tabellino di gara storica."""
    title: str
    description: str = Field(min_length=50, max_length=220)
    slug: str = Field(pattern=r"^partite/\d{4}-\d{4}/[a-z0-9-]+$")
    match_date: date
    season_slug: str = Field(pattern=r"^stagioni/\d{4}-\d{4}$")
    competition: str
    matchday: str
    stadium_slug: str = Field(pattern=r"^stadio/[a-z0-9-]+$")
    attendance: Optional[int] = Field(default=None, ge=0)
    referee: str
    catania_is_home: bool = True
    score_home: int = Field(ge=0)
    score_away: int = Field(ge=0)
    scorers: list[GoalEvent] = Field(default_factory=list)
    sources: list[SourceCitationPayload] = Field(min_length=1)
    image_credits: list[ImageCreditPayload] = Field(default_factory=list)

    @model_validator(mode="after")
    def verify_score_matches_goals(self) -> "MatchReportPayload":
        total_goals = self.score_home + self.score_away
        if len(self.scorers) != total_goals:
            raise ValueError(
                f"Il numero di marcatori registrati ({len(self.scorers)}) non coincide "
                f"con la somma delle reti del risultato ({self.score_home}-{self.score_away} = {total_goals})."
            )
        return self


# --- 3D. Tifoseria Organizzata ---

StadiumSectorType = Literal[
    "Curva Sud - Anello Inferiore",
    "Curva Sud - Anello Superiore",
    "Curva Nord",
    "Tribuna B",
    "Tribuna A",
]

class UltrasGroupPayload(BaseModel):
    title: str
    description: str = Field(min_length=50, max_length=220)
    slug: str = Field(pattern=r"^tifoseria/(curva-sud|curva-nord|tribune)/[a-z0-9-]+$")
    foundation_year: int = Field(ge=1960, le=2026)
    founder_slug: Optional[str] = Field(default=None, pattern=r"^tifoseria/biografie/[a-z0-9-]+$")
    origin_district: str
    stadium_sector: StadiumSectorType
    international_ties: list[str] = Field(default_factory=list)
    sources: list[SourceCitationPayload] = Field(min_length=1)
    image_credits: list[ImageCreditPayload] = Field(default_factory=list)


# --- 3E. Segnalazione Esterna & Fact-Checking AI ---

class ExternalCorrectionSubmission(BaseModel):
    """Input inviato da un utente esterno tramite il form 'Segnala correzione'."""
    target_page_slug: str = Field(min_length=3)
    reporter_name_or_email: Optional[str] = Field(default=None, description="Opzionale (GDPR minimization)")
    claim_type: Literal["Errore Statistico", "Data o Fatto Storico", "Nuova Fonte Bibliografica", "Credito Fotografico"]
    current_text_excerpt: str = Field(min_length=5)
    proposed_correction: str = Field(min_length=10)
    supporting_source: SourceCitationPayload = Field(
        description="Fonte obbligatoria a supporto della segnalazione per attivare il FactCheckAgent"
    )


class FactCheckVerdictPayload(BaseModel):
    """Esito prodotto da FactCheckAgent prima della revisione finale dell'operatore umano."""
    submission_slug: str
    verdict: Literal["VERIFIED_ACCEPT", "REJECTED_UNSUBSTANTIATED", "NEEDS_HUMAN_ARBITRATION"]
    confidence_score: float = Field(ge=0.0, le=1.0)
    verification_rationale: str = Field(min_length=20)
    proposed_markdown_diff: Optional[str] = None


# =====================================================================
# 4. LINTER DI CONFORMITÀ DEL VAULT MARKDOWN (QA & EU COMPLIANCE GATE)
# =====================================================================

@dataclass
class VaultAuditResult:
    file_path: str
    is_valid: bool
    errors: list[str]


class VaultComplianceLinter:
    """Verifica che tutti i file Markdown in content/ rispettino SCHEMA.md, le fonti e l'accessibilità."""

    FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", re.DOTALL)
    IMAGE_MD_RE = re.compile(r"!\[(.*?)\]\((.*?)\)")

    @classmethod
    def audit_file(cls, md_path: Path) -> VaultAuditResult:
        errors: list[str] = []
        raw = md_path.read_text(encoding="utf-8")
        match = cls.FRONTMATTER_RE.match(raw)
        if not match:
            return VaultAuditResult(str(md_path), False, ["Frontmatter YAML mancante o malformato."])

        fm_raw, body = match.group(1), match.group(2)
        try:
            fm = yaml.safe_load(fm_raw)
        except Exception as exc:
            return VaultAuditResult(str(md_path), False, [f"Errore sintassi YAML: {exc}"])

        if not isinstance(fm, dict):
            return VaultAuditResult(str(md_path), False, ["Frontmatter YAML non è un dizionario chiave-valore."])

        # 1. Campi obbligatori di base
        for req_key in ("title", "description", "slug", "entity_type", "status"):
            if not fm.get(req_key):
                errors.append(f"Campo frontmatter obbligatorio mancante: '{req_key}'")

        # 2. Obbligo citazione fonti (Art. 70 L. 633/1941) per tutte le voci enciclopediche
        entity_type = fm.get("entity_type", "")
        if entity_type not in ("home_portal", "legal_compliance", "feedback_portal", "section_index"):
            sources = fm.get("sources")
            if not isinstance(sources, list) or len(sources) == 0:
                errors.append("Conformità Copyright violata: array 'sources' mancante o vuoto nel Frontmatter.")
            if "## Fonti" not in body:
                errors.append("Conformità Copyright violata: sezione '## Fonti e Bibliografia' mancante nel corpo Markdown.")

        # 3. Controllo Accessibilità Immagini (WCAG 2.1 AA alt text) e Crediti Fotografici
        for alt_text, img_url in cls.IMAGE_MD_RE.findall(body):
            if len(alt_text.strip()) < 10:
                errors.append(
                    f"Accessibilità WCAG 2.1 AA violata: l'immagine '{img_url}' ha un attributo alt assente o troppo corto ('{alt_text}')."
                )
            credits = fm.get("image_credits", [])
            if not isinstance(credits, list) or len(credits) == 0:
                errors.append(
                    f"Diritto d'Autore violato: l'immagine '{img_url}' è priva di voce in 'image_credits' nel Frontmatter."
                )

        # 4. Controllo Tabelle GFM: rileva wikilinks [[slug|Testo]] con pipe non sottoposto a escape dentro righe di tabella
        for line_num, line in enumerate(body.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                # Cerca [[...|...]] in cui il pipe NON è preceduto da backslash
                unescaped = re.findall(r"\[\[[^\]]*(?<!\\)\|[^\]]*\]\]", stripped)
                if unescaped:
                    errors.append(
                        f"Riga {line_num}: Wikilink con pipe non sottoposto a escape in tabella GFM: {unescaped}. Usa [[slug\\|Testo]]."
                    )

        # 5. Controllo Fonti Web: tutte le fonti web citate devono contenere un hyperlink HTTP/HTTPS alla fonte originale
        for line_num, line in enumerate(body.splitlines(), start=1):
            stripped = line.strip()
            if any(dom in stripped.lower() for dom in ["mimmorapisarda.it", "tuttoilcataniaminutoperminuto.it", "calciocatania.com"]):
                if not re.search(r"https?://", stripped):
                    errors.append(
                        f"Riga {line_num}: Fonte web priva di link HTTP/HTTPS alla fonte originale: '{stripped}'."
                    )

        return VaultAuditResult(str(md_path), len(errors) == 0, errors)
