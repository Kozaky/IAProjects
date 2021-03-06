import random
import Genetic_Implementation
from operator import itemgetter

distances = {
    'DeHu' : 175,
    'DeSe' : 25,
    'DeMa' : 525,
    'DeZa' : 775,
    'DeCa' : 75,
    'SeSe' : 0,
    'SeHu' : 150,
    'SeCa' : 100,
    'SeZa' : 750,
    'SeMa' : 500,
    'SeDe' : 25,
    'HuHu' : 0,
    'HuSe' : 150,
    'HuCa' : 90,
    'HuZa' : 850,
    'HuMa' : 620,
    'HuDe' : 175,
    'CaCa' : 0,
    'CaSe' : 100,
    'CaHu' : 90,
    'CaZa' : 900,
    'CaMa' : 600,
    'CaDe' : 75,
    'ZaZa' : 0,
    'ZaCa' : 900,
    'ZaSe' : 750,
    'ZaMa' : 200,
    'ZaHu' : 850,
    'ZaDe' : 775,
    'MaMa' : 0,
    'MaSe' : 500,
    'MaZa' : 200,
    'MaHu' : 620,
    'MaCa' : 600,
    'MaDe' : 525,
}

genes = {
    0 : 'Se',
    1 : 'Ca',
    2 : 'Hu',
    3 : 'Za',
    4 : 'Ma',
    5 : 'De'
}

pop_size = 10
delivery_capacity = 4  # The number of trucks will be the lenght / capacity
lenght = 5            # we visit deposit twice, once for each truck
max_iterations = 1000
crossover_rate = 0.75
mutation_rate = 0.1



def generate_population():
    ''' Genereates a random population '''
    chromos, chromo = [], []
    for eachChromo in range(pop_size):
        chromo = []
        for city in range(lenght):
            chromo = random.sample(range(5), 5)
        chromos.append(chromo)


    return chromos

def translate_population(pop):
    ''' Convert the numbers into Strings so the population is most understandable '''
    chromo, chromos = [], []
    for row in pop:
        chromo = []
        for value in row:
            chromo.append(genes.get(value))

        chromos.append(chromo)

    return chromos

def translate_populationAux(pop):
    ''' Convert the numbers into Strings so the population is most understandable '''
    chromo, chromos = [], []
    for row in pop:
        chromo = []
        cont = 0
        for value in row:
            if cont == 0:
                chromo.append('De')
            chromo.append(genes.get(value))
            cont += 1
            if (cont % delivery_capacity == 0 and cont != 0) or cont == lenght:
                chromo.append('De')


        chromos.append(chromo)
    return chromos

def cal_fitness(chromo):
    cont = 0
    i = 1
    while i <= lenght:
        if i == 1:
            cont += distances.get('De' + chromo[i - 1])
            cont += distances.get(chromo[i - 1] + chromo[i])

        elif i % delivery_capacity == 0:
            cont += distances.get(chromo[i - 1] + 'De')
            cont += distances.get('De' + chromo[i])
        elif i == lenght:
            cont += distances.get(chromo[i - 1] + 'De')
        else:
            cont += distances.get(chromo[i - 1] + chromo[i])

        i += 1


    if len(set(chromo)) != len(chromo):
        cont += 1500

    return cont


def rank_fitness(chromos):
    proteins, score = [], []
    translated = translate_population(chromos)

    cont = 0
    for chromo in translated:
        protein = chromo
        proteins.append(chromos[cont])
        score.append(cal_fitness(protein))
        cont += 1


    popAndScore = zip(proteins, score)
    rankedPop = sorted(popAndScore, key = itemgetter(-1), reverse = False )

    return rankedPop


def breed(ch1, ch2):
  #print 'ch1 y ch2 breed', ch1, ch2
  newCh1, newCh2 = ch1, ch2
  if random.random() < crossover_rate:
      chooser = random.randint(1, 2)
      if chooser == 3:
          #print 'partially mapped'
          newCh1, newCh2 = Genetic_Implementation.partially_mapped_crossover(ch1, ch2)
      elif chooser == 2:
          #print 'table'
          table = Genetic_Implementation.create_table(ch1, ch2)
          newCh1 = Genetic_Implementation.edge_recombination(table)
          newCh2 = ch2
      elif chooser == 1:
          #print 'order'
          newCh1, newCh2 = Genetic_Implementation.order_crossover(ch1, ch2)

  elif random.random() < mutation_rate:
      chooser = random.randint(1, 3)
      newCh1, newCh2 = ch1, ch2
      if chooser == 3:
          #print 'permutation'
          newCh1 = Genetic_Implementation.permutation_mutation(newCh1)
          newCh2 = Genetic_Implementation.permutation_mutation(newCh2)
      elif chooser == 2:
          #print 'swap'
          newCh1 = Genetic_Implementation.swap_mutation(newCh1)
          newCh2 = Genetic_Implementation.swap_mutation(newCh2)
      elif chooser == 1:
          #print 'inversion'
          newCh1 = Genetic_Implementation.inversion_mutation(newCh1)
          newCh2 = Genetic_Implementation.inversion_mutation(newCh2)

  return newCh1, newCh2


def iteratePop (rankedPop):
  fitnessScores = [ item[-1] for item in rankedPop ]
  rankedChromos = [ item[0] for item in rankedPop ]
  #print 'ranked chromos', rankedChromos
  elite = int(lenght * 0.15)

  if elite % 2 == 0:
     elite += 1

  newpop = rankedChromos[:elite]
  begin =  1
  while len(newpop) < pop_size - 1:
      #print 'lenght newpop: ', len(newpop), 'lenght rankedChromos: ', len(rankedChromos)
      #print 'RankedChromos: ', rankedChromos
      #print 'newPop: ', newpop
      #print 'Begin: ', begin
      ch1, ch2 = [], []
      ch1 = rankedChromos[begin]
      begin += 1
      ch2 = rankedChromos[begin]
      #print 'CH1 & CH2', ch1, ch2
      ch1, ch2 = breed (ch1, ch2)
      #print 'CH1 & CH2 after Breed', ch1, ch2
      newpop.append(ch1)
      newpop.append(ch2)
      begin += 1

  #print 'NewPop out', newpop
  return newpop


def pop_with_fitness(chromos):
    proteins, score = [], []
    translated = translate_population(chromos)
    translatedAux = translate_populationAux(chromos)

    cont = 0
    for chromo in translated:
        protein = chromo
        proteins.append(translatedAux[cont])
        score.append(cal_fitness(protein))
        cont += 1

    popAndScore = zip(proteins, score)
    #rankedPop = sorted(popAndScore, key = itemgetter(-1), reverse = False )
    return popAndScore

def main():
    chromos = generate_population()
    iterations = 0

    while iterations != max_iterations:
        chromos = rank_fitness(chromos)
        chromos = iteratePop(chromos)
        #print 'Chromos main: ', chromos
        iterations += 1

    return pop_with_fitness(chromos)




#aux = generate_population()
#print aux
#print translate_population(aux)
#tra = translate_population(aux)
#print 'hola' , tra[0][1] + tra[0][2]
#print cal_fitness(tra[0])
#print rank_fitness(aux)
#print 'population', generate_population()
outPop = main()
print 'Output Population: ', outPop
