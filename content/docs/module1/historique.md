---
title: "Les idées historiques importantes"
weight: 60
---

# Historique

## Une conférence en temps de crise

D'une manière similaire à la conférence de Dartmouth qui a dans un sens inauguré
le domaine de l'intelligence artificielle en 1956, on peut dire que c'est la
conférence NATO, organisée en 1968 en Allemagne, qui a inauguré le génie
logiciel en tant que domaine. Dans cette conférence, il a été question pour la
première fois d'une "crise du logiciel", qui commençait à se profiler dans
l'horizon culturel et technologique de l'époque.

Voici un programme typique de l'époque, en Fortran, un langage de programmation
dit de "troisième génération", conçu par IBM en 1956.

{{% hint info %}}

La première génération de langages correspond aux "langages machine", soit celui
des microprocesseurs, essentiellement composé de nombres entiers, tandis que la
deuxième génération correspond à l'assembleur, une couche syntaxique
relativement mince, au-dessus du langage machine, pour le rendre plus "digeste"
pour les programmeurs, car il décompose les nombres purs du langage machine en
leurs différentes fonctions: instructions, opérandes, adresses, etc. La
troisième génération correspond à la famille assez large des langages compilés,
de plus haut niveau, qui sont conçus pour être "transformés" (compilés) _vers_
un langage de plus bas niveau, plus proche de la machine donc.

{{% /hint %}}

```fortran
      PROGRAM AVG_LINE_SUMS
      REAL TOTAL, LSUM, AVG
      INTEGER NLINES
      CHARACTER*256 LINE

      TOTAL  = 0.0
      NLINES = 0

   10 CONTINUE
      READ(*,'(A)',END=900,ERR=800) LINE
      CALL SUMCSV_GOTO(LINE, LSUM)
      TOTAL  = TOTAL + LSUM
      NLINES = NLINES + 1
      GO TO 10

  800 CONTINUE
      GO TO 10

  900 CONTINUE
      IF (NLINES .EQ. 0) THEN
         PRINT *, 'NO INPUT'
      ELSE
         AVG = TOTAL / FLOAT(NLINES)
         PRINT *, 'AVG_OF_LINE_SUMS=', AVG
      ENDIF
      END


      SUBROUTINE SUMCSV_GOTO(LINE, SUM)
      CHARACTER*(*) LINE
      REAL SUM
      CHARACTER*32 TOK
      CHARACTER*1 C
      INTEGER I, J, L, VAL

      SUM = 0.0
      TOK = ' '
      I   = 1
      J   = 0
      L   = LEN(LINE)

   20 CONTINUE
      IF (I .GT. L+1) GO TO 200

      IF (I .LE. L) THEN
         C = LINE(I:I)
      ELSE
         C = ','            ! sentinel comma to flush last token
      ENDIF

      IF (C .EQ. ' ') GO TO 90

      IF (C .NE. ',') GO TO 60

C     --- end of token (comma) ---
      IF (J .EQ. 0) GO TO 90
      READ(TOK,*,ERR=85) VAL
      SUM = SUM + VAL
   85 CONTINUE
      TOK = ' '
      J   = 0
      GO TO 90

C     --- accumulate token character ---
   60 CONTINUE
      J = J + 1
      IF (J .LE. 32) TOK(J:J) = C

   90 CONTINUE
      I = I + 1
      GO TO 20

  200 CONTINUE
      RETURN
      END
```

Voici l'équivalent en COBOL, un langage compilé et de type "business", datant de 1960 :

```cobol
       IDENTIFICATION DIVISION.
       PROGRAM-ID. AVG-LINE-SUMS.

       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT SYSIN ASSIGN TO KEYBOARD
               ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD  SYSIN.
       01  IN-REC              PIC X(256).

       WORKING-STORAGE SECTION.
       77  TOTAL               PIC S9(12)V9(4) VALUE 0.
       77  LINE-SUM            PIC S9(12)V9(4) VALUE 0.
       77  AVG                 PIC S9(12)V9(4) VALUE 0.
       77  LINE-COUNT          PIC 9(9)        VALUE 0.

       77  I                   PIC 9(4) VALUE 0.
       77  C                   PIC X    VALUE SPACE.
       77  TOK-LEN             PIC 9(2) VALUE 0.
       01  TOKEN               PIC X(32) VALUE SPACES.
       77  NUM                 PIC S9(12)V9(4) VALUE 0.

       PROCEDURE DIVISION.
       MAIN.
           OPEN INPUT SYSIN
           GO TO READ-LOOP.

       READ-LOOP.
           READ SYSIN
               AT END GO TO FINISH
           END-READ
           MOVE 0      TO LINE-SUM
           MOVE 1      TO I
           MOVE 0      TO TOK-LEN
           MOVE SPACES TO TOKEN
           GO TO PARSE-CHAR.

       PARSE-CHAR.
           IF I > 256 GO TO FLUSH-TOKEN
           MOVE IN-REC(I:1) TO C

           IF C = SPACE GO TO NEXT-CHAR
           IF C = ","   GO TO FLUSH-TOKEN

           ADD 1 TO TOK-LEN
           IF TOK-LEN <= 32
               MOVE C TO TOKEN(TOK-LEN:1)
           END-IF
           GO TO NEXT-CHAR.

       FLUSH-TOKEN.
           IF TOK-LEN = 0 GO TO AFTER-FLUSH
           COMPUTE NUM = FUNCTION NUMVAL(TOKEN)
           ADD NUM TO LINE-SUM
           MOVE 0      TO TOK-LEN
           MOVE SPACES TO TOKEN

       AFTER-FLUSH.
           IF I > 256 GO TO END-LINE
           GO TO NEXT-CHAR.

       NEXT-CHAR.
           ADD 1 TO I
           GO TO PARSE-CHAR.

       END-LINE.
           ADD LINE-SUM TO TOTAL
           ADD 1 TO LINE-COUNT
           GO TO READ-LOOP.

       FINISH.
           CLOSE SYSIN
           IF LINE-COUNT = 0
               DISPLAY "NO INPUT"
               STOP RUN
           END-IF
           COMPUTE AVG = TOTAL / LINE-COUNT
           DISPLAY "AVG_OF_LINE_SUMS=" AVG
           STOP RUN.
```

Et finalement une version moderne du même algorithme écrit en Python, un langage
très populaire de nos jours, créé par Guido Van Rossum en 1991 :

```python
import sys

def sum_csv_ints(line: str) -> int:
    return sum(int(tok) for tok in line.strip().split(",") if tok != "")

def main() -> None:
    total = 0
    nlines = 0

    for line in sys.stdin:
        total += sum_csv_ints(line)
        nlines += 1

    print("NO INPUT" if nlines == 0 else f"AVG_OF_LINE_SUMS={total / nlines}")

if __name__ == "__main__":
    main()
```

La crise du logiciel n'était pas causée exclusivement par la qualité ou la
puissance des langages de programmation de l'époque, mais c'est certain que ces
aspects y ont joué un rôle.