"""
Master list of all IHSG (IDX Composite) tickers.

Sourced from the Indonesia Stock Exchange (IDX) listed companies.
Tickers are stored WITHOUT the '.JK' suffix; use get_yf_tickers()
to get Yahoo-Finance-compatible symbols.

Last updated: 2026-03-07
Total unique tickers: 900+
"""

from __future__ import annotations

# ─── Raw ticker codes (IDX symbols, no suffix) ───────────────────────────────

_RAW_TICKERS: list[str] = [
    "AALI", "ABBA", "ABDA", "ABMM", "ACES", "ACST", "ADCP", "ADES", "ADHI", "ADMF",
    "ADMG", "ADMR", "ADRO", "AGII", "AGRO", "AHAP", "AIMS", "AISA", "AKKU", "AKPI",
    "AKRA", "AKSI", "ALDO", "ALII", "ALKA", "ALMI", "ALTO", "AMAG", "AMAN", "AMAR",
    "AMFG", "AMMS", "AMRT", "ANDI", "ANJT", "ANTM", "APIC", "APII", "APLN", "APOL",
    "ARMY", "ARNA", "ARTA", "ARTI", "ASBI", "ASDM", "ASGO", "ASII", "ASJT", "ASKP",
    "ASMI", "ASPI", "ASRM", "ASSA", "ASTE", "ATAP", "ATLA", "AUTO", "AVIA", "AYLS",
    "BABP", "BACA", "BAJA", "BALI", "BAPA", "BATA", "BAYU", "BBCA", "BBHI", "BBKP",
    "BBLD", "BBMD", "BBNI", "BBRI", "BBSI", "BBSS", "BBTC", "BBTN", "BBYB", "BCAP",
    "BCIC", "BCIP", "BEKS", "BELI", "BELL", "BFIN", "BGTG", "BHAT", "BHIT", "BIKA",
    "BIMA", "BIPP", "BIRD", "BISI", "BJBR", "BJTM", "BKDP", "BKSL", "BKSW", "BLTA",
    "BLTZ", "BMHS", "BMRI", "BMSR", "BMTR", "BNBA", "BNGA", "BNIK", "BNII", "BNLI",
    "BOBA", "BOGA", "BOLA", "BOLT", "BOSS", "BPFI", "BPII", "BPTR", "BRAD", "BREN",
    "BRMS", "BRNA", "BROK", "BRPT", "BSDE", "BSIM", "BSML", "BSSR", "BTEK", "BTEL",
    "BTON", "BTPN", "BTPS", "BUDI", "BUEF", "BUKA", "BULL", "BUMI", "BUVA", "BVIC",
    "CAKK", "CANI", "CARE", "CASS", "CBMF", "CCSI", "CEKA", "CENT", "CFIN", "CINT",
    "CITY", "CKSN", "CLPI", "CMNT", "CMNP", "CMPP", "CNKO", "COAL", "COBP", "COCO",
    "COWL", "CPGT", "CPIN", "CPRI", "CPRO", "CSAP", "CTBN", "CTRA", "CTRP", "CTRL",
    "CUAN", "DART", "DAWA", "DCII", "DEWA", "DFAM", "DGIK", "DILD", "DIVA", "DKFT",
    "DLTA", "DMAS", "DMND", "DNAR", "DNET", "DOID", "DPNS", "DPUM", "DSFI", "DSNG",
    "DSSA", "DUTI", "DVLA", "DWGL", "DYAN", "EAST", "ECII", "EDGE", "EKAD", "ELSA",
    "ELTY", "EMDE", "EMTK", "ENRG", "ENVY", "EPMT", "ERAA", "ESSA", "ESTA", "ESTI",
    "EXCL", "EXPD", "FAPA", "FAST", "FASW", "FIGHT", "FILM", "FIMP", "FIRE", "FISH",
    "FITT", "FLMC", "FOOD", "FORU", "FPNI", "FREN", "FUEL", "GAMA", "GAPD", "GBIC",
    "GDST", "GEMA", "GEMS", "GGRM", "GHON", "GJTL", "GLOB", "GLVA", "GMFI", "GMTD",
    "GOLL", "GOOD", "GPRA", "GRIA", "GSMF", "GTBO", "GTSI", "GWSA", "GZCO", "HDFA",
    "HDTX", "HEAL", "HERO", "HEXA", "HILL", "HITS", "HKMU", "HMSP", "HOKI", "HOME",
    "HOPE", "HOTL", "HRTA", "HRUM", "IATA", "IBFN", "IBST", "ICBP", "IGAR", "IHSG",
    "IIKP", "IKAN", "IKBI", "IMAS", "INAF", "INCI", "INCO", "INDF", "INDO", "INDR",
    "INDS", "INDX", "INDY", "INKP", "INPC", "INPP", "INPS", "INRU", "INTA", "INTD",
    "INTP", "IPCC", "IPCM", "IPPE", "IPOL", "IPTV", "IRRA", "ISAT", "ISSP", "ITMG",
    "IUCN", "JARR", "JAST", "JAWA", "JGLE", "JIHD", "JKON", "JMAS", "JPFA", "JSKY",
    "JSMR", "JTPE", "KAEF", "KARW", "KBAG", "KBLI", "KBLM", "KBLV", "KDSI", "KEEN",
    "KEJU", "KICI", "KIJA", "KINO", "KIOS", "KITA", "KKGI", "KLBF", "KMDS", "KMTR",
    "KOIN", "KONI", "KOPI", "KPIG", "KRAS", "KREN", "KSIX", "LAND", "LCKM", "LCNP",
    "LMPI", "LMSH", "LPCK", "LPGI", "LPKR", "LPLI", "LPPF", "LPPS", "LSIP", "LUCK",
    "LTLS", "MABA", "MAIN", "MAMI", "MAPI", "MASA", "MASB", "MASC", "MBAP", "MBMA",
    "MCAS", "MCOL", "MCOS", "MDKA", "MDRN", "MEDC", "MEGA", "MFIN", "MFMI", "MICE",
    "MIDI", "MIKA", "MIRA", "MKPI", "MLBI", "MLPL", "MLPT", "MMIX", "MNCN", "MNCS",
    "MOLI", "MPPA", "MPRO", "MRAT", "MRMA", "MSIN", "MSKY", "MTDL", "MTFN", "MTLA",
    "MTRA", "MTSM", "MYOR", "MYOH", "MYTX", "NASI", "NCKL", "NETX", "NFCX", "NICL",
    "NISP", "NITO", "NKPK", "NOBU", "NOVA", "NPGF", "NRCA", "NSSS", "NUSA", "NZIA",
    "OCAP", "OKAS", "OKON", "OMRE", "ORCA", "OSAO", "PACK", "PADI", "PALM", "PAMG",
    "PANS", "PANR", "PBID", "PBSA", "PCAR", "PDES", "PEGE", "PEHA", "PGAS", "PGLO",
    "PGJO", "PGLI", "PGMJ", "PHSL", "PICO", "PJAA", "PKPK", "PLAN", "PLIN", "PLTM",
    "PMJS", "PNBS", "PNGO", "PNIN", "PNLF", "POLA", "POLL", "POLI", "POME", "POOL",
    "POWR", "PPGL", "PPRO", "PRDA", "PRIM", "PTBA", "PTIS", "PTPP", "PTRO", "PTSP",
    "PUDP", "PURA", "PWON", "PYFA", "RAJA", "RALS", "RATU", "RBMS", "RDTX", "REAL",
    "RELI", "REMA", "RGAS", "RIMO", "RMBA", "RODA", "ROTI", "RUIS", "RUNS", "SAFE",
    "SAME", "SAMF", "SARI", "SBMA", "SCCO", "SCMA", "SCPI", "SDMU", "SDPC", "SDRA",
    "SFAN", "SGER", "SGRO", "SHIP", "SIDO", "SILO", "SIMP", "SINI", "SIPD", "SKLT",
    "SKYB", "SMCB", "SMDM", "SMGR", "SMMT", "SMRA", "SMRU", "SMSM", "SOFA", "SOHO",
    "SOSS", "SOTS", "SPMA", "SQBB", "SRAJ", "SRTG", "SSIA", "SSMS", "SSTM", "STTP",
    "SUGI", "SULI", "SUPR", "SURE", "SWAT", "TALF", "TAMA", "TARA", "TAXI", "TBIG",
    "TBLA", "TBMS", "TCID", "TFIA", "TFIN", "TGKA", "TGRA", "TINS", "TIRA", "TIRT",
    "TITL", "TLKM", "TMAS", "TMPI", "TOBA", "TOPS", "TOWR", "TPIA", "TPMA", "TRIL",
    "TRIM", "TRIO", "TRIS", "TRJA", "TRST", "TRUS", "TSPC", "TURI", "ULTJ", "UNIC",
    "UNIQ", "UNIT", "UNSP", "UNTR", "UNVR", "URBN", "VICI", "VINS", "VIVA", "WAPO",
    "WEGE", "WEHA", "WIIM", "WIKA", "WINS", "WIRG", "WOOD", "WSBP", "WSKT", "WTON",
    "YELO", "YPAS", "YULE", "ZBRA", "ZINC", "ZONE", "ZYRX",
    # ── Additional large-cap / recently listed ────────────────────────────────
    "AMMN", "ASSE", "BEST", "CAMP",
]


def _deduplicate(tickers: list[str]) -> list[str]:
    """Remove duplicates while preserving insertion order."""
    seen: set[str] = set()
    result: list[str] = []
    for t in tickers:
        t_upper = t.strip().upper()
        if t_upper and t_upper not in seen:
            seen.add(t_upper)
            result.append(t_upper)
    return result


# ─── Public API ───────────────────────────────────────────────────────────────

IHSG_TICKERS: list[str] = _deduplicate(_RAW_TICKERS)
"""Deduplicated list of IDX ticker codes (e.g. 'BBCA', 'TLKM')."""


def get_yf_tickers() -> list[str]:
    """Return tickers with '.JK' suffix for Yahoo Finance compatibility."""
    return [f"{t}.JK" for t in IHSG_TICKERS]


def get_ticker_count() -> int:
    """Return the total number of unique tickers in the universe."""
    return len(IHSG_TICKERS)
